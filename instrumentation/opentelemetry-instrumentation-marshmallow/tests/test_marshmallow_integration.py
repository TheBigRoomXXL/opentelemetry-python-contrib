
from unittest import mock

import pytest

from opentelemetry import trace
from opentelemetry.instrumentation.marshmallow import MarshmallowInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, export
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.test.test_base import TestBase

from marshmallow import Schema, fields, EXCLUDE

class FixtureSchema(Schema):
    a = fields.Str()
    b = fields.Int()
    c = fields.Boolean()




class TestMarshmallowInstrumentor(TestBase):
    schema = FixtureSchema()
    schema_only = FixtureSchema(only=['a'])
    schema_exclude = FixtureSchema(exclude=['a'])
    schema_many = FixtureSchema(many=True)
    schema_unknown = FixtureSchema(unknown=EXCLUDE)
    schema_partial = FixtureSchema(partial=True)
    schema_load_only = FixtureSchema(load_only=['a'])
    schema_dump_only = FixtureSchema(dump_only=['b'])
    schemas = (
        schema, schema_only, schema_exclude, schema_load_only, schema_dump_only, schema_unknown, schema_partial
    )

    def setUp(self):
        super().setUp()
        MarshmallowInstrumentor().instrument()

    def tearDown(self):
        super().tearDown()
        MarshmallowInstrumentor().uninstrument()


    def test_trace_on_load(self):
        data = {
            "a": "blablabla",
            "b": 4,
            "c": True
        }
        self.schema.load(data)
        spans = self.memory_exporter.get_finished_spans()
        print(spans)
        self.assertEqual(len(spans), 1)

        print(spans[0])
        print(spans[0].name)
        print(spans[0].kind)
        print(spans[0].__dict__)
        print(spans[0].attributes)


        self.assertEqual(spans[0].name, "load")
        self.assertEqual(spans[0].kind, trace.SpanKind.CLIENT)
        self.assertEqual(spans[0].attributes, [])


    def test_trace_on_loads(self):
        pass
    
    def test_trace_on_dump(self):
        pass


    def test_trace_on_dumps(self):
        pass

    
    def test_trace_on_validate(self):
        pass


    def test_trace_on_pre_dump(self):
        pass

    def test_trace_on_pre_load(self):
        pass


    def test_trace_on_post_dump(self):
        pass


    def test_trace_on_post_load(self):
        pass


    def test_trace_on_validate_schema(self):
        pass
    
    def test_only_attribute(self):
        pass
    
    def test_exclude_attribute(self):
        pass
    
    def test_many_attribute(self):
        pass
    
    def test_load_only_attribute(self):
        pass

    def test_dump_only_attribute(self):
        pass

    
    def test_not_recording(self):
        pass
        # mock_tracer = mock.Mock()
        # mock_span = mock.Mock()
        # mock_context = mock.Mock()
        # mock_span.is_recording.return_value = False
        # mock_context.__enter__ = mock.Mock(return_value=mock_span)
        # mock_context.__exit__ = mock.Mock(return_value=None)
        # mock_tracer.start_span.return_value = mock_context
        # mock_tracer.start_as_current_span.return_value = mock_context
        # with mock.patch("opentelemetry.trace.get_tracer") as tracer:
        #     tracer.return_value = mock_tracer
        #     engine = create_engine("sqlite:///:memory:")
        #     SQLAlchemyInstrumentor().instrument(
        #         engine=engine,
        #         tracer_provider=self.tracer_provider,
        #     )
        #     cnx = engine.connect()
        #     cnx.execute("SELECT	1 + 1;").fetchall()
        #     self.assertFalse(mock_span.is_recording())
        #     self.assertTrue(mock_span.is_recording.called)
        #     self.assertFalse(mock_span.set_attribute.called)
        #     self.assertFalse(mock_span.set_status.called)

    def test_instrument_twice(self):
        pass


    def test_custom_tracer_provider(self):
        pass
        # provider = TracerProvider(
        #     resource=Resource.create(
        #         {
        #             "service.name": "test",
        #             "deployment.environment": "env",
        #             "service.version": "1234",
        #         },
        #     ),
        # )
        # provider.add_span_processor(
        #     export.SimpleSpanProcessor(self.memory_exporter)
        # )

        # SQLAlchemyInstrumentor().instrument(tracer_provider=provider)
        # from sqlalchemy import create_engine  # pylint: disable-all

        # engine = create_engine("sqlite:///:memory:")
        # cnx = engine.connect()
        # cnx.execute("SELECT	1 + 1;").fetchall()
        # spans = self.memory_exporter.get_finished_spans()

        # self.assertEqual(len(spans), 2)
        # self.assertEqual(spans[0].resource.attributes["service.name"], "test")
        # self.assertEqual(
        #     spans[0].resource.attributes["deployment.environment"], "env"
        # )
        # self.assertEqual(
        #     spans[0].resource.attributes["service.version"], "1234"
        # )

    def test_uninstrument(self):
        pass


    def test_instrument_schema(self):
        pass


    def test_uninstrument_schema(self):
        pass

