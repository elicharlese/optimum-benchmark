from dataclasses import dataclass, MISSING
from logging import getLogger

import time
import psutil
import platform
from omegaconf import DictConfig
from transformers import __version__ as transformers_version
from optimum.version import __version__ as optimum_version

from src.utils import get_gpu, get_gpu_ram_mb, bytes_to_mega_bytes
from src.backend.base import BackendConfig
from src.benchmark.inference import BenchmarkConfig


LOGGER = getLogger("experiment")


@dataclass
class ExperimentConfig:
    # MODEL CONFIGURATION
    # Name of the model to run (bert-base-uncased, ...)
    model: str = MISSING  # type: ignore
    # Task on which the model is run (sequence-classification, ...)
    task: str = MISSING  # type: ignore
    # Device on which the model is loaded and run (cpu, cuda, ...)
    device: str = MISSING  # type: ignore

    # BACKEND CONFIGURATION
    # The backend to use for recording timing (pytorch, onnxruntime, ...)
    backend: BackendConfig = MISSING  # type: ignore

    # BENCHMARK CONFIGURATION
    # The kind of benchmark to run (inference, training, ...)
    benchmark: BenchmarkConfig = MISSING  # type: ignore

    # EXPERIMENT CONFIGURATION
    # Experiment name
    experiment_name: str = MISSING  # type: ignore
    # Experiment identifier (timestamp)
    experiment_datetime: str = time.strftime("%Y-%m-%d_%H:%M:%S")

    # ENVIRONMENT CONFIGURATION
    environment: DictConfig = DictConfig(
        {
            "optimum_version": optimum_version,
            "transformers_version": transformers_version,
            "python_version": platform.python_version(),
            "system": platform.system(),
            "architecture": platform.architecture()[0],
            "machine": platform.machine(),
            "cpu": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "cpu_ram_mb": bytes_to_mega_bytes(psutil.virtual_memory().total),
            "gpu": get_gpu(),
            "gpu_ram_mb": get_gpu_ram_mb(),
        }
    )
