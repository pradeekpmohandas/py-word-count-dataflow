import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class WordCountOptions(PipelineOptions):
    """Custom options for the Word Count pipeline."""
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input', help='Input file path', required=True)
        parser.add_argument('--output', help='Output file path', required=True)

def run():
    # Define custom pipeline options
    options = WordCountOptions()

    # Create the pipeline
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | 'Read Input File' >> beam.io.ReadFromText(options.input)
            | 'Split Words' >> beam.FlatMap(lambda line: line.split())
            | 'Pair With One' >> beam.Map(lambda word: (word, 1))
            | 'Count Words' >> beam.CombinePerKey(sum)
            | 'Write Output File' >> beam.io.WriteToText(options.output)
        )

if __name__ == '__main__':
    run()
