"""TestSpecConfigParser Example"""
from tspec_config_parser import TestSpecConfigParser

def main():
    """Parse Spec Config File"""
    # Initialize TestSpecConfigParser
    parser = TestSpecConfigParser('sample.tspec')

    # Generate TestSpec Object
    test_spec = parser.generate_tspec()
    print test_spec

    # Convert TestSpec to CSV file
    test_spec.convert_to_csv()

if __name__ == '__main__':
    main()
