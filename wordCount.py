import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

class WordCountOptions(PipelineOptions):
    """Custom options for the Word Count pipeline."""
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input', help='Input file path', default=None)
        parser.add_argument('--output', help='Output file path', default=None)

def run():
    # Define custom pipeline options
    options = WordCountOptions()
    options.view_as(SetupOptions).save_main_session = True

    # Extract runtime parameters
    input_path = options.input
    output_path = options.output

    # Create the pipeline
    with beam.Pipeline(options=options) as pipeline:
        # Read input only if the input path is provided
        lines = (
            pipeline
            | 'Read Input File' >> beam.io.ReadFromText(input_path)
            if input_path
            else pipeline | 'Create Empty Input' >> beam.Create([])
        )

        (
            lines
            | 'Split Words' >> beam.FlatMap(lambda line: line.split())
            | 'Pair With One' >> beam.Map(lambda word: (word, 1))
            | 'Count Words' >> beam.CombinePerKey(sum)
            | 'Write Output File' >> beam.io.WriteToText(output_path)
            if output_path
            else lines  # Avoid writing output if no path is provided
        )

if __name__ == '__main__':
    run()
