import time
from concurrent.futures import ThreadPoolExecutor

class CryptoDataFetcher:
    def __init__(self, sources):
        self.sources = sources
        self.session = None

    def fetch_data(self, source):
        start_time = time.time()
        # Simulating data fetching with sleep
        time.sleep(1)  # Simulate network delay
        print(f'Data fetched from {source}')
        return {source: f'data from {source}', 'response_time': time.time() - start_time}

    def fetch_all(self):
        results = []
        with ThreadPoolExecutor(max_workers=len(self.sources)) as executor:
            future_to_source = {executor.submit(self.fetch_data, source): source for source in self.sources}
            for future in future_to_source:
                source = future_to_source[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    print(f'Error fetching data from {source}: {e}')
        return results

# Usage example
if __name__ == '__main__':
    fetcher = CryptoDataFetcher(['source1', 'source2', 'source3'])
    data = fetcher.fetch_all()
    print(data)