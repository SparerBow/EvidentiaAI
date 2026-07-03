import argparse
import logging
import os
import sys

# ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.pubmed_agent import search_and_save


def configure_logging(level: str = 'INFO', logfile: str | None = None):
    numeric = getattr(logging, level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    if logfile:
        handlers.append(logging.FileHandler(logfile))
    logging.basicConfig(level=numeric, format='%(asctime)s %(levelname)s %(name)s: %(message)s', handlers=handlers)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run PubMed search and save results')
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--max', '-m', type=int, default=20, help='Max results')
    parser.add_argument('--api-key', help='NCBI API key (overrides NCBI_API_KEY env var)')
    parser.add_argument('--email', help='Contact email (overrides NCBI_EMAIL env var)')
    parser.add_argument('--logfile', help='Optional log file path')
    parser.add_argument('--log', default='INFO', help='Log level')

    args = parser.parse_args(argv)
    configure_logging(args.log, args.logfile)

    api_key = args.api_key or os.environ.get('NCBI_API_KEY')
    email = args.email or os.environ.get('NCBI_EMAIL')

    search_and_save(args.query, max_results=args.max, api_key=api_key, email=email)


if __name__ == '__main__':
    main()
