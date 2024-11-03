import torch
import os

class CUDASetup:
    def __init__(self):
        self.cuda_available = torch.cuda.is_available()
        self.cuda_version = torch.version.cuda

    def check_cuda(self):
        print(f"CUDA Available: {self.cuda_available}")
        print(f"CUDA Version: {self.cuda_version}")

    def setup(self):
        self.check_cuda()
        if self.cuda_available:
            print("Installing CuGraph...")
            os.system("conda install -c rapidsai -c conda-forge -c nvidia cugraph cuda-version=12.3 -y")
            print("Complete.")
        else:
            print("CUDA not available.")

        print("Installing Library...")
        os.system("pip install ogb")
        os.system("pip install torch_geometric")
        os.system("pip install graphistry")
        os.system("pip install scikit-network")
        print("Complete.")
