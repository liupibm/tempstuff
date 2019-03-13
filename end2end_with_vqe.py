# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import logging
logging.basicConfig(level=logging.DEBUG)

from parameterized import parameterized
import qiskit
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms.adaptive import VQE
from qiskit.aqua.components.variational_forms import RYRZ
from qiskit.aqua.components.optimizers import COBYLA, SPSA, AQGD
from qiskit.chemistry.drivers import HDF5Driver
from qiskit.chemistry.core import Hamiltonian, TransformationType, QubitMappingType

driver = HDF5Driver(hdf5_input='/Users/liup/quantum/qiskit-chemistry/test/test_driver_hdf5.hdf5')
qmolecule = driver.run()

core = Hamiltonian(transformation=TransformationType.FULL,
                   qubit_mapping=QubitMappingType.PARITY,
                   two_qubit_reduction=True,
                   freeze_core=False,
                   orbital_reduction=[],
                   max_workers=4)

algo_input = core.run(qmolecule)
reference_energy = -1.857275027031588
optimizer = 'AQGD'


if optimizer == 'COBYLA':
    optimizer = COBYLA()
    optimizer.set_options(maxiter=1000)
elif optimizer == 'SPSA':
    optimizer = SPSA(max_trials=2000)
elif optimizer == 'AQGD':
    optimizer = AQGD()

mode = 'paulis'
backend = qiskit.BasicAer.get_backend('statevector_simulator')
shots = 1
ryrz = RYRZ(algo_input.qubit_op.num_qubits, depth=3, entanglement='full')
vqe = VQE(algo_input.qubit_op, ryrz, optimizer, mode, aux_operators=algo_input.aux_ops)
quantum_instance = QuantumInstance(backend, shots=shots)

import time
start = time.time()
results = vqe.run(quantum_instance)
print(results['energy'])

end = time.time()
print(optimizer)
print(end-start)
# self.assertAlmostEqual(, self.reference_energy, places=4)

#-1.8572740378003958
#AQGD
#110.03657007217407


#  'functionality and more.', DeprecationWarning)
#-1.8572750246754892
#<qiskit.aqua.components.optimizers.cobyla.COBYLA object at 0x10d90b940>
#44.02508020401001
