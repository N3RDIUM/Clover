# Comms.py
# This file communicates with the Clover API.

import requests
import json
import time
import os
import threading
import click

# multithreaded downloader
class Downloader:
    def __init__(self, url, path, filename, nthreads=128):
        self.url = url
        self.path = path
        self.filename = filename
        self.n_threads = nthreads
        self.thread_results = {}
        self.threads = []
        self.cache_folder = self.filename.replace('/', '_').replace('.', '_') + '/'
        self.download()

    def download_part(self, url, start, end, index):
        resp = requests.get(url, headers={'Range': 'bytes={}-{}'.format(start, end)}, stream=True)
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                self.thread_results[index][0] += str(chunk)
        # write to file
        with open(self.path + self.cache_folder + str(index) + '.txt', 'w') as f:
            f.write(self.thread_results[index][0])
        self.thread_results[index][0] = True                

    def download(self):
        r = requests.head(self.url)
        total_size = int(r.headers['Content-Length'])
        part_size = total_size // self.n_threads
        os.mkdir(self.path + self.cache_folder)
        for i in range(self.n_threads):
            self.thread_results[i] = ["", False]
            start = part_size * i
            end = part_size * (i + 1) - 1
            func = lambda:self.download_part(self.url, start, end, i)
            thread = threading.Thread(target=func, daemon=True)
            thread.start()
            self.threads.append(thread)

        # wait for all threads to finish
        while True:
            total_complete = 0
            for i in range(self.n_threads):
                if self.thread_results[i][0]:
                    total_complete += 1
            if total_complete == self.n_threads:
                break
            # print progress
            print(f'\rDownloading {total_complete}/{self.n_threads}', end='')

        # write to file
        with open(self.path + self.filename, 'w') as f:
            for i in range(self.n_threads):
                try:
                    with open(self.path + self.cache_folder + str(i) + '.txt', 'r') as f2:
                        f.write(f2.read())
                except FileNotFoundError:
                    pass
                os.remove(self.path + self.cache_folder + str(i) + '.txt')
        os.rmdir(self.path + self.cache_folder)
        # join threads
        for thread in self.threads:
            thread.join()

if __name__ == '__main__':
    dwnldr = Downloader('https://atom-installer.github.com/v1.60.0/AtomSetup-x64.exe?s=1646703880&ext=.exe', './', 'atomSetup.exe', 512)
