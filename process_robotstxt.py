#!/usr/bin/env python3

import os
import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process robotstxt.paths file from Common Crawl')
    parser.add_argument('--input', default='robotstxt.paths', help='Path to robotstxt.paths file')
    parser.add_argument('--output-dir', default='downloads', help='Directory to save downloaded files')
    parser.add_argument('--download', action='store_true', help='Actually download the files (default: only show URLs)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of files to process')
    args = parser.parse_args()
    
    # Create output directory if downloading
    if args.download and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Read the robotstxt.paths file
    with open(args.input, 'r') as f:
        lines = f.readlines()
    
    print(f"Found {len(lines)} robotstxt files in the list")
    
    # Process each line
    processed = 0
    for line in lines:
        # Remove any leading numbers/arrows and whitespace
        path = line.strip()
        if '→' in path:
            path = path.split('→')[1].strip()
        
        # Generate URLs
        http_url = f"https://data.commoncrawl.org/{path}"
        s3_url = f"s3://commoncrawl/{path}"
        
        print(f"\nPath: {path}")
        print(f"HTTP URL: {http_url}")
        print(f"S3 URL: {s3_url}")
        
        # Download if requested
        if args.download:
            # Extract filename from path
            filename = os.path.basename(path)
            output_path = os.path.join(args.output_dir, filename)
            
            print(f"Downloading to: {output_path}")
            try:
                response = requests.get(http_url, stream=True)
                response.raise_for_status()
                
                with open(output_path, 'wb') as out_f:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_f.write(chunk)
                print(f"✓ Downloaded {filename}")
            except Exception as e:
                print(f"✗ Failed to download: {e}")
        
        processed += 1
        if args.limit and processed >= args.limit:
            print(f"\nReached limit of {args.limit} files")
            break
    
    print(f"\nProcessed {processed} files")
    if args.download:
        print(f"Downloaded files are in: {args.output_dir}")

if __name__ == "__main__":
    main()
