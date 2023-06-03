# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import wraps
from collections.abc import Callable
from typing import ParamSpec, TypeVar, Collection, Any
from copy import deepcopy
from logging import getLogger

from opentelemetry.trace import get_tracer
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.marshmallow.package import _instruments
from opentelemetry.instrumentation.marshmallow.version import __version__

from marshmallow import Schema, decorators


P = ParamSpec("P")
R = TypeVar("R")

class MarshmallowInstrumentor(BaseInstrumentor):

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")

        self._tracer = get_tracer(__name__, __version__, tracer_provider)
        self._instrumented_schemas = []
        self._original_hooks = deepcopy(decorators.set_hook)

        self.instrument_schema(Schema)
        self._instrument_decorators()

    def instrument_schema(self, schema: Schema) -> None:
        self._instrumented_schemas.append((schema, deepcopy(schema)))
        schema.load = self._traced(schema.load)
        schema.dump = self._traced(schema.dump)
        schema.loads = self._traced(schema.loads)
        schema.dumps = self._traced(schema.dumps)
        schema.validate = self._traced(schema.validate)

    def _instrument_decorators(self) -> Callable[P, R]:
        """Wrap user hooks with tracing by overloading """

        @wraps(decorators.set_hook)
        def set_hook_with_tracing(func):
            func = self._traced(func)
            return func

        return set_hook_with_tracing
    
    def _traced(self, func: Callable[P, R]) -> Callable[P, R]:
        """Wrap a schema method with tracing and add attributes"""

        @wraps(func)
        def method_with_tracing(_self: Schema, *args: P.args, **kwargs: P.kwargs) -> R:
            with self._tracer.start_as_current_span(
                func.__name__, set_status_on_exception=False
            ) as span:
                if span.is_recording():
                    span.set_attribute("schema", _self.__class__.__name__)
                    span.set_attribute("schema.fields", str(list(_self.fields)))
                    span.set_attribute("schema.many", _self.many)
                    span.set_attribute("schema.partial", _self.partial)
                    span.set_attribute("schema.unknown", _self.unknown)
                    span.set_attribute("schema.ordered", _self.ordered)

                result = func(_self, *args, **kwargs)
                return result

        return method_with_tracing
    
    def _uninstrument(self, *args, **kwargs) -> None:
        """Uninstrument the library by setting back schema and 
        hooks to there original state"""
        for schema, original_state in self._instrumented_schemas:
            schema = original_state  # noqa: F841
        decorators.set_hook = self._original_hooks