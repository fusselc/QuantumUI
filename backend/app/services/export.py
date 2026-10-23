import json
import urllib.parse
from typing import Dict, Any, Optional
from app.models.schemas import ExperimentRecord

class ExportService:
    @staticmethod
    def to_jupyter_notebook(record: ExperimentRecord) -> Dict[str, Any]:
        """Generates clean Jupyter Notebook (.ipynb) JSON structure."""
        code_to_run = record.user_edited_code or record.generated_code
        shots = record.execution_config.shots

        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# QuantumUI Experiment: {record.prompt_text}\n",
                    f"**Experiment ID:** `{record.experiment_id}`  \n",
                    f"**Created:** {record.created_at.isoformat()}  \n",
                    f"**Provenance:** Qiskit v{record.provenance.qiskit_version}, Adapter: `{record.provenance.adapter_used}`  \n",
                    "\n",
                    "---",
                    "### Plain-Language Summary\n",
                    f"{record.explanation_by_level.beginner if record.explanation_by_level else 'No explanation generated.'}\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Install dependencies if running on Google Colab or new virtualenv\n",
                    "!pip install -q qiskit qiskit-aer matplotlib\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    code_to_run + "\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Execute on Qiskit Aer Simulator\n",
                    "from qiskit_aer import AerSimulator\n",
                    "from qiskit.visualization import plot_histogram\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "simulator = AerSimulator()\n",
                    f"job = simulator.run(qc, shots={shots})\n",
                    "result = job.result()\n",
                    "counts = result.get_counts()\n",
                    "print('Measurement Counts:', counts)\n",
                    "\n",
                    "# Visualize histogram\n",
                    "plot_histogram(counts)\n",
                    "plt.show()\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### Technical & Physics Analysis\n",
                    f"{record.explanation_by_level.technical if record.explanation_by_level else ''}\n"
                ]
            }
        ]

        return {
            "cells": cells,
            "metadata": {
                "language_info": {
                    "name": "python",
                    "version": "3.11"
                },
                "orig_nbformat": 4
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }

    @staticmethod
    def get_google_colab_url(record: ExperimentRecord, github_repo: Optional[str] = None) -> str:
        """Generates one-click Google Colab launch URL."""
        if github_repo:
            return f"https://colab.research.google.com/github/{github_repo}/blob/main/experiments/{record.experiment_id}.ipynb"
        return f"https://colab.research.google.com/#create=true"
