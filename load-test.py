#!/usr/bin/env python3
"""
Load testing script to demonstrate ECS auto scaling behavior.
Requires: pip install requests
"""

import requests
import threading
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# Replace with your ALB DNS name from Terraform output
ALB_URL = "http://ecs-fargate-alb-1462992800.us-east-2.elb.amazonaws.com"

def make_request(session, url, request_id):
    """Make a single HTTP request"""
    try:
        response = session.get(url, timeout=10)
        print(f"Request {request_id}: Status {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Request {request_id}: Error - {e}")
        return None

def load_test(duration_minutes=5, concurrent_requests=50):
    """Run load test for specified duration with concurrent requests"""
    print(f"Starting load test against {ALB_URL}")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Concurrent requests: {concurrent_requests}")
    print("-" * 50)
    
    end_time = time.time() + (duration_minutes * 60)
    request_count = 0
    
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            while time.time() < end_time:
                # Submit batch of requests
                futures = []
                for i in range(concurrent_requests):
                    future = executor.submit(make_request, session, ALB_URL, request_count + i)
                    futures.append(future)
                
                # Wait for batch to complete
                for future in futures:
                    future.result()
                
                request_count += concurrent_requests
                print(f"Completed {request_count} requests...")
                time.sleep(1)  # Brief pause between batches
    
    print(f"Load test completed. Total requests: {request_count}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
    else:
        duration = 5
    
    if len(sys.argv) > 2:
        concurrent = int(sys.argv[2])
    else:
        concurrent = 50
    
    load_test(duration, concurrent)