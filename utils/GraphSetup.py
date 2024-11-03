import torch
import os
import subprocess
from tqdm import tqdm
import time


class CUDASetup:
    def __init__(self):
        self.cuda_available = torch.cuda.is_available()
        self.cuda_version = torch.version.cuda

    def check_cuda(self):
        print(f"CUDA Available: {self.cuda_available}")
        print(f"CUDA Version: {self.cuda_version}")

    def install_library(self, command):
        # Chạy lệnh cài đặt mà không hiển thị log
        with open(os.devnull, 'w') as devnull:
            subprocess.run(command, stdout=devnull, stderr=devnull, shell=True)

    def setup(self):
        self.check_cuda()

        if self.cuda_available:
            print("Installing CuGraph...")
            conda_command = "conda install rapidsai::cugraph -y"
            self.install_library(conda_command)
            print("CuGraph installation complete.")
        else:
            print("CUDA not available.")

            # Danh sách các thư viện cần cài đặt
        libraries = [
            "ogb",
            "torch_geometric",
            "graphistry",
            "scikit-network",
            "pip install graphistry  "
        ]

        print("Installing Libraries...")
        for library in tqdm(libraries, desc="Installing Libraries", unit="library"):
            self.install_library(f"pip install {library}")

        print("All installations complete.")