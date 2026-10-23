from typing import Dict, List
from app.models.schemas import Template, ExplanationByLevel, DifficultyLevel

TEMPLATES_CATALOG: Dict[str, Template] = {
    "coin-flipper": Template(
        template_id="coin-flipper",
        name="The Quantum Coin Flipper",
        description="Creates a 50/50 superposition on a single qubit using a Hadamard gate, yielding true quantum randomness.",
        difficulty=DifficultyLevel.BEGINNER,
        category="Foundations",
        prompt_text="Create a single-qubit quantum coin flipper using a Hadamard gate, then measure the qubit.",
        suggestion_chips=[
            "Change shot count to 2048",
            "Add a second Hadamard gate to observe interference",
            "View statevector telemetry"
        ],
        qiskit_code=(
            "from qiskit import QuantumCircuit\n\n"
            "# 1 Qubit, 1 Classical bit\n"
            "qc = QuantumCircuit(1, 1)\n"
            "qc.h(0)  # Apply Hadamard gate to create (|0> + |1>)/sqrt(2)\n"
            "qc.measure(0, 0)  # Measure qubit 0 into classical bit 0\n"
        ),
        circuit_description="Qubit 0 initialized to |0>. Hadamard gate applied to Qubit 0. Measurement applied to Qubit 0 into Classical Bit 0.",
        explanation_by_level=ExplanationByLevel(
            beginner="This experiment places a single coin (qubit) into a spinning state in mid-air (superposition). Until measured, it is in a combination of heads (0) and tails (1). When measured, it lands on 0 or 1 with equal 50% probability.",
            intermediate="A single qubit initialized in state |0> is transformed by the Hadamard gate (H) into the superposition state (|0> + |1>)/sqrt(2). Measurement collapses this wave function with equal probability |c_i|^2 = 0.5 to state |0> or |1>.",
            technical="Applies unitary operator H = 1/sqrt(2) * [[1, 1], [1, -1]] mapping basis state |0> -> |+>. Computational basis measurement projects the density operator onto |0><0| or |1><1| with equal eigenvalues."
        )
    ),

    "quantum-link": Template(
        template_id="quantum-link",
        name="The Quantum Link (Bell State)",
        description="Entangles two qubits so that measuring one instantly determines the state of the other (Bell state |Phi+>).",
        difficulty=DifficultyLevel.BEGINNER,
        category="Foundations",
        prompt_text="Create an entangled Bell State on two qubits using a Hadamard and a CNOT gate, then measure both.",
        suggestion_chips=[
            "Try changing CNOT control target",
            "Swap initial state with X gate",
            "Measure on noisy hardware"
        ],
        qiskit_code=(
            "from qiskit import QuantumCircuit\n\n"
            "# 2 Qubits, 2 Classical bits\n"
            "qc = QuantumCircuit(2, 2)\n"
            "qc.h(0)       # Superposition on qubit 0\n"
            "qc.cx(0, 1)   # CNOT with control 0 and target 1 (entanglement)\n"
            "qc.measure([0, 1], [0, 1])  # Measure both qubits\n"
        ),
        circuit_description="Qubits 0 and 1 initialized. Hadamard applied to Qubit 0. CNOT applied with Control Qubit 0 and Target Qubit 1. Measurements applied to both qubits.",
        explanation_by_level=ExplanationByLevel(
            beginner="This links two coins together. If you spin one and entangle them, they will always land on the exact same face (both 0 or both 1), even if separated across galaxies. Measuring one instantly reveals the other.",
            intermediate="Constructs the maximally entangled Bell state |Phi+> = (|00> + |11>)/sqrt(2). Partial trace over either qubit yields a maximally mixed state, yet joint measurements show 100% computational correlation.",
            technical="Applies H_0 followed by CX_{0->1} creating state vector |Psi> = 1/sqrt(2)(|00> + |11>). The density matrix rho = |Psi><Psi| yields perfect joint correlation expectations Tr(rho * (Z_0 (x) Z_1)) = 1.0."
        )
    ),

    "phase-shift": Template(
        template_id="phase-shift",
        name="The Phase Shift",
        description="Demonstrates how rotating a qubit's phase around the Z-axis (Bloch Sphere) alters interference without changing individual 50/50 measurement probabilities.",
        difficulty=DifficultyLevel.BEGINNER,
        category="Foundations",
        prompt_text="Initialize a qubit, put it into superposition, apply a pi/4 Phase Shift (P gate), and measure.",
        suggestion_chips=[
            "Increase rotation to pi/2 (S gate)",
            "Increase rotation to pi (Z gate)",
            "Add a second Hadamard to detect phase"
        ],
        qiskit_code=(
            "from qiskit import QuantumCircuit\nimport math\n\n"
            "# 1 Qubit, 1 Classical bit\n"
            "qc = QuantumCircuit(1, 1)\n"
            "qc.h(0)  # Superposition\n"
            "qc.p(math.pi / 4, 0)  # Apply Phase shift of pi/4\n"
            "qc.measure(0, 0)\n"
        ),
        circuit_description="Qubit 0 initialized. Hadamard gate applied to Qubit 0. Phase gate P(pi/4) applied to Qubit 0. Measurement applied to Qubit 0.",
        explanation_by_level=ExplanationByLevel(
            beginner="Phase is like turning a clock hand in the quantum world. Rotating the phase changes the relative angle of the quantum state on the Bloch Sphere without changing the immediate 50/50 likelihood of measuring 0 or 1.",
            intermediate="The P(theta) gate applies unitary diag(1, e^(i*theta)) to state (|0> + |1>)/sqrt(2), producing (|0> + e^(i*pi/4)|1>)/sqrt(2). Measurement in the computational basis remains 50/50 because |e^(i*theta)|^2 = 1.",
            technical="Unitary transformation P(theta) = exp(i*theta/2 * (I - Z)). Relative phase shift transforms equatorial Bloch vector from |+> towards |+i> without altering Z-axis projector probabilities."
        )
    ),

    "quantum-interference": Template(
        template_id="quantum-interference",
        name="Quantum Interference",
        description="Demonstrates constructive and destructive wave interference by applying two Hadamard gates in sequence.",
        difficulty=DifficultyLevel.BEGINNER,
        category="Foundations",
        prompt_text="Demonstrate quantum interference using two consecutive Hadamard gates to return a qubit deterministically to state 0.",
        suggestion_chips=[
            "Add a Pauli-X gate between Hadamards",
            "Add a Z gate between Hadamards to see constructive interference on state 1"
        ],
        qiskit_code=(
            "from qiskit import QuantumCircuit\n\n"
            "qc = QuantumCircuit(1, 1)\n"
            "qc.h(0)  # First split: creates superposition (|0> + |1>)/sqrt(2)\n"
            "qc.h(0)  # Second split: waves interfere destructively for |1> and constructively for |0>\n"
            "qc.measure(0, 0)\n"
        ),
        circuit_description="Qubit 0 initialized. First Hadamard gate applied. Second Hadamard gate applied. Measurement applied to Qubit 0.",
        explanation_by_level=ExplanationByLevel(
            beginner="Imagine two water waves meeting. If their peaks line up, they build a giant wave; if peak meets valley, they cancel out. The second Hadamard cancels the probability of tails (1) and restores heads (0) with 100% certainty.",
            intermediate="H * H = I (the identity matrix). The amplitude for state |1> cancels out via destructive interference ((1/2) - (1/2) = 0), while amplitude for |0> undergoes constructive interference ((1/2) + (1/2) = 1).",
            technical="Applies H^2 = I on computational basis state |0>. The unitary product ensures 100% fidelity recovery of the initial pure state rho = |0><0|."
        )
    ),

    "phase-flip": Template(
        template_id="phase-flip",
        name="Phase Flip & Superposition (State |->)",
        description="Applies a Pauli-X followed by a Hadamard gate to create the orthogonal superposition state |-> = (|0> - |1>)/sqrt(2).",
        difficulty=DifficultyLevel.BEGINNER,
        category="Foundations",
        prompt_text="Create the minus superposition state |-> using an X gate followed by a Hadamard gate.",
        suggestion_chips=[
            "Observe difference from |+> state",
            "Add a Z gate to flip back to |+>"
        ],
        qiskit_code=(
            "from qiskit import QuantumCircuit\n\n"
            "qc = QuantumCircuit(1, 1)\n"
            "qc.x(0)  # Flip |0> to |1>\n"
            "qc.h(0)  # Transform |1> into |-> = (|0> - |1>)/sqrt(2)\n"
            "qc.measure(0, 0)\n"
        ),
        circuit_description="Qubit 0 initialized. Pauli-X gate applied to Qubit 0. Hadamard gate applied to Qubit 0. Measurement applied to Qubit 0.",
        explanation_by_level=ExplanationByLevel(
            beginner="This creates an alternate quantum coin flip where the quantum wave is 'upside down' (negative phase). Measuring it still gives a 50/50 outcome, but it behaves differently when interacting with other quantum gates.",
            intermediate="Initializes qubit to |1> using Pauli-X (NOT), then applies Hadamard: H|1> = (|0> - |1>)/sqrt(2) (the |-> state). It is an eigenstate of the Pauli-X operator with eigenvalue -1.",
            technical="Unitary sequence H * X on basis |0> produces state |->. Density matrix off-diagonal coherence terms are negative real (-0.5), pointing to (-1, 0, 0) on the Bloch Sphere."
        )
    )
}

def get_template(template_id: str) -> Template:
    return TEMPLATES_CATALOG.get(template_id)

def list_templates() -> List[Template]:
    return list(TEMPLATES_CATALOG.values())
