# Hybrid QAOA for Satellite Network Routing

This repository implements a hybrid quantum-classical optimization framework 
for evaluating QAOA-based routing under NISQ constraints.

## Features
- Max-Cut → QUBO mapping
- QUBO → Ising Hamiltonian transformation
- Shallow-depth QAOA implementation
- Classical optimization loop (COBYLA)
- Noiseless vs noisy simulation comparison
- Telemetry-weighted routing graphs
- Scalability analysis (N = 2–8 nodes)

## Experimental Highlights
- Approximation ratio degradation with scaling
- Noise-induced objective collapse
- Telemetry-grounded feasibility evaluation

## Tools Used
- Qiskit
- NumPy
- Matplotlib
- NetworkX

## Run Instructions
pip install -r requirements.txt
python experiments/run_noiseless.py

## Repository Structure

code/
    Core QAOA implementations and classical baselines

data/
    Telemetry-derived edge weights

results/
    Final plots and experiment outputs
