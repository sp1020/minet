import argparse
from minet import interaction_analysis
from minet import network


def main():
    parser = argparse.ArgumentParser(prog='MINet')
    # Refer https://docs.python.org/3/library/argparse.html

    # sub-commands
    subparsers = parser.add_subparsers(
        dest='command', title='sub-commands', help='sub-command help')

    # sub-parser
    subparsers.add_parser('interaction', parents=[interaction_analysis.parser],
                          help='Interaction analysis')
    subparsers.add_parser('network', parents=[network.parser],
                          help='Network analysis')

    # parse arguments
    args = parser.parse_args()
    cmd = args.command

    # Load feature table
    if cmd == 'interaction':
        analyzer = interaction_analysis.Analyzer()
        analyzer.load_feature_table(args.input)
        analyzer.evaluate_feature_association(args.output)
    elif cmd == 'network':
        nt = network.Network()
        nt.load_interaction_results(args.input, args.fdr_co, args.fdr_qt, args.co_type, args.qt_type, args.pval_dir)
        nt.write_graph(args.output)
