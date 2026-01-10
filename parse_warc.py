#!/usr/bin/env python3

import os
import gzip
import argparse
from io import BytesIO

# Check if warcio is available, if not, we'll use a basic parser
try:
    from warcio.archiveiterator import ArchiveIterator
    has_warcio = True
    print("Using warcio library for parsing")
except ImportError:
    has_warcio = False
    print("warcio library not found, using basic parser")
    print("Consider installing it with: pip install warcio")


def parse_warc_basic(file_path):
    """Basic WARC parser for demonstration"""
    print(f"\n=== Basic WARC Parser ===")
    print(f"Processing file: {file_path}")
    
    with gzip.open(file_path, 'rb') as f:
        content = f.read()
    
    # Split by WARC record delimiter
    records = content.split(b'\r\n\r\n')
    print(f"Found approximately {len(records)} record segments")
    
    # Look for robots.txt content
    for i, record in enumerate(records[:5]):  # Show first 5 segments
        if b'robots.txt' in record:
            print(f"\n--- Record {i} (contains robots.txt) ---")
            # Try to find content
            if b'Content-Length:' in record:
                parts = record.split(b'Content-Length:')
                if len(parts) > 1:
                    # Extract content length
                    len_part = parts[1].split(b'\r\n')[0].strip()
                    try:
                        content_len = int(len_part)
                        # Look for actual content
                        content_start = record.find(b'\r\n\r\n', record.find(b'Content-Length:')) + 4
                        if content_start > 0:
                            robots_content = record[content_start:content_start + content_len]
                            print(f"Content-Length: {content_len}")
                            print(f"Robots.txt content:\n{robots_content[:500].decode('utf-8', errors='ignore')}...")
                    except ValueError:
                        pass
    
    print("\n=== Basic Parser Complete ===")


def parse_warc_warcio(file_path):
    """Parse WARC using warcio library"""
    print(f"\n=== Advanced WARC Parser (using warcio) ===")
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'rb') as stream:
        iterator = ArchiveIterator(stream)
        record_count = 0
        robots_count = 0
        
        for record in iterator:
            record_count += 1
            
            if record.rec_type == 'response':
                # Check if this is a robots.txt response
                uri = record.rec_headers.get_header('WARC-Target-URI', '')
                if 'robots.txt' in uri:
                    robots_count += 1
                    
                    if robots_count <= 3:  # Show first 3 robots.txt entries
                        print(f"\n--- Robots.txt Entry #{robots_count} ---")
                        print(f"URI: {uri}")
                        print(f"WARC-Type: {record.rec_type}")
                        print(f"WARC-Date: {record.rec_headers.get_header('WARC-Date', 'N/A')}")
                        
                        # Get HTTP status
                        http_headers = record.http_headers
                        if http_headers:
                            print(f"HTTP-Status: {http_headers.get_statuscode()}")
                            print(f"Content-Type: {http_headers.get_header('Content-Type', 'N/A')}")
                            
                        # Get content
                        content = record.content_stream().read()
                        print(f"Content-Length: {len(content)}")
                        print(f"Content:\n{content.decode('utf-8', errors='ignore')[:500]}...")
        
        print(f"\n=== Parser Summary ===")
        print(f"Total records: {record_count}")
        print(f"Robots.txt entries: {robots_count}")


def extract_all_robots(file_path, output_dir):
    """Extract all robots.txt content to separate files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n=== Extracting all robots.txt entries ===")
    print(f"Input: {file_path}")
    print(f"Output directory: {output_dir}")
    
    if has_warcio:
        with open(file_path, 'rb') as stream:
            iterator = ArchiveIterator(stream)
            robots_count = 0
            
            for record in iterator:
                if record.rec_type == 'response':
                    uri = record.rec_headers.get_header('WARC-Target-URI', '')
                    if 'robots.txt' in uri:
                        robots_count += 1
                        # Extract domain from URI
                        domain = uri.split('//')[-1].split('/')[0].replace(':', '_').replace('.', '_')
                        filename = f"{robots_count:04d}_{domain}_robots.txt"
                        output_path = os.path.join(output_dir, filename)
                        
                        content = record.content_stream().read()
                        
                        with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
                            f.write(f"# URI: {uri}\n")
                            f.write(f"# WARC-Date: {record.rec_headers.get_header('WARC-Date', 'N/A')}\n")
                            f.write(content.decode('utf-8', errors='ignore'))
                        
                        print(f"Extracted: {filename} ({len(content)} bytes)")
        
        print(f"\n✓ Extracted {robots_count} robots.txt entries")
    else:
        print("warcio library required for extraction, please install it first")


def main():
    parser = argparse.ArgumentParser(description='Parse Common Crawl WARC files containing robots.txt')
    parser.add_argument('file_path', help='Path to the WARC.gz file')
    parser.add_argument('--extract', action='store_true', help='Extract all robots.txt entries to separate files')
    parser.add_argument('--output-dir', default='extracted_robots', help='Directory for extracted robots.txt files')
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        return
    
    # Check if file is gzipped
    if not args.file_path.endswith('.gz'):
        print("Warning: File does not appear to be gzipped")
    
    # Choose parsing method
    if has_warcio:
        if args.extract:
            extract_all_robots(args.file_path, args.output_dir)
        else:
            parse_warc_warcio(args.file_path)
    else:
        parse_warc_basic(args.file_path)
        if args.extract:
            print("Extraction requires warcio library")


if __name__ == "__main__":
    main()
