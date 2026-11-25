"""Finite quantum-channel diagnostics and ordinary memory counterexamples."""
from itertools import product
import json

import numpy as np

I = np.eye(2)
X = np.array([[0., 1.], [1., 0.]])
Y = np.array([[0., -1j], [1j, 0.]])
Z = np.diag([1., -1.])
PHI = np.array([1., 0., 0., 1.])/np.sqrt(2.)
BELL = np.outer(PHI, PHI)


def correlations(state, observables):
    return [float(np.trace(state@np.kron(left,right)).real) for left,right in observables]


def partial_transpose(state, right_dimension):
    dimension = state.shape[0]//right_dimension
    return state.reshape(dimension,right_dimension,dimension,right_dimension).transpose(0,3,2,1).reshape(state.shape)


def damping_threshold():
    survival, bath_ground = .3, .6
    thermal_cross = bath_ground*(1-bath_ground)*(1-survival)**2
    coherence_threshold = np.sqrt(thermal_cross/survival)
    populations = np.array([bath_ground+(1-bath_ground)*survival,
                            (1-bath_ground)*(1-survival), bath_ground*(1-survival),
                            1-bath_ground+bath_ground*survival])
    minima, positivity = [], []
    coherences = [.5, .8]
    for coherence in coherences:
        choi = np.diag(populations/2)
        choi[0,3] = choi[3,0] = coherence*np.sqrt(survival)/2
        positivity.append(float(np.min(np.linalg.eigvalsh(choi))))
        minima.append(float(np.min(np.linalg.eigvalsh(partial_transpose(choi,2)))))
    return dict(survival=survival, bath_ground_probability=bath_ground,
                coherence_threshold=float(coherence_threshold), coherence_settings=coherences,
                choi_minimum_eigenvalues=positivity, partial_transpose_minima=minima)


def bell_correlations():
    visibility = .68
    state = visibility*BELL+(1-visibility)*np.eye(4)/4
    values = correlations(state, [(X,X),(Y,Y),(Z,Z)])
    reconstructed = (1+values[0]-values[1]+values[2])/4
    dephased = np.diag(np.diag(state))
    example_plus = (np.eye(4)+.5*np.kron(Y,Y))/4
    example_minus = (np.eye(4)-.5*np.kron(Y,Y))/4
    return dict(correlations=values, overlap_from_settings=reconstructed,
                omitted_axis_overlap_difference=float(abs(PHI@(example_plus-example_minus)@PHI)),
                direct_overlap=float(PHI@state@PHI),
                dephased_overlap=float(PHI@dephased@PHI),
                common_population_error=float(np.max(abs(np.diag(state)-np.diag(dephased)))))


def two_basis_benchmark():
    output_copies = (np.diag([1.,0.,0.,1.]))/2
    score = lambda state: .5+sum(correlations(state,[(X,X),(Z,Z)]))/4
    target_visibility = .6
    target = target_visibility*BELL+(1-target_visibility)*np.eye(4)/4
    z_only_score = (1+correlations(output_copies,[(Z,Z)])[0])/2
    return dict(classical_two_basis_score=score(output_copies), classical_z_only_score=z_only_score,
                partially_coherent_two_basis_score=score(target),
                excess_over_exact_separable_bound=score(target)-.75)


def misregistered_axes():
    separable = np.diag([1.,0.,0.,0.])
    duplicated = correlations(separable,[(Z,Z),(Z,-Z),(Z,Z)])
    trusted = correlations(separable,[(X,X),(Y,Y),(Z,Z)])
    fake = (1+duplicated[0]-duplicated[1]+duplicated[2])/4
    honest = (1+trusted[0]-trusted[1]+trusted[2])/4
    reported_axes = np.array([[0,0,1],[0,0,1],[0,0,1]])
    return dict(reported_values=duplicated, reported_overlap=fake, true_overlap=honest,
                trusted_direct_overlap=float(PHI@separable@PHI),
                independently_measured_axis_gram_rank=int(np.linalg.matrix_rank(reported_axes@reported_axes.T)))


def reset_residual():
    leak_power = .02
    field_transmission = np.sqrt(leak_power)
    kraus_zero = np.diag([1.,field_transmission])
    kraus_one = np.array([[0.,np.sqrt(1-leak_power)],[0.,0.]])
    operators = [kraus_zero,kraus_one]
    states = [(I+X)/2,(I-X)/2]
    measurements = [sum(float(np.trace(X@operator@state@operator.T)) for operator in operators) for state in states]
    occupancy = sum(float((operator@np.diag([0.,1.])@operator.T)[1,1]) for operator in operators)
    return dict(leak_power=occupancy, surviving_orthogonal_quadratures=measurements,
                paired_quadrature_gap=measurements[0]-measurements[1],
                predicted_amplitude_gap=float(2*field_transmission),
                naive_power_gap=2*leak_power)


def flagged_erasure():
    efficiency = .2
    successful = np.zeros((6,6))
    live = [0,1,3,4]
    successful[np.ix_(live,live)] = efficiency*BELL
    flagged = successful + np.diag([0,0,(1-efficiency)/2,0,0,(1-efficiency)/2])
    unconditional = efficiency*BELL+(1-efficiency)*np.eye(4)/4
    minimum_flagged = float(np.min(np.linalg.eigvalsh(partial_transpose(flagged,3))))
    minimum_fallback = float(np.min(np.linalg.eigvalsh(partial_transpose(unconditional,2))))
    return dict(efficiency=efficiency, success_conditioned_overlap=float(PHI@(successful[np.ix_(live,live)]/efficiency)@PHI),
                flagged_pt_minimum=minimum_flagged, fallback_pt_minimum=minimum_fallback,
                fallback_overlap=float(PHI@unconditional@PHI), flagged_trace=float(np.trace(flagged)))


def phase_probe():
    theta = .37
    candidate, alternative = [np.diag([1.,np.exp(1j*sign*theta)]) for sign in (1.,-1.)]
    old_states = [(I+Z)/2,(I-Z)/2,(I+X)/2]
    def record(unitary, state, measurement):
        return float(np.trace(measurement@unitary@state@unitary.conj().T).real)
    old_gap = max(abs(record(candidate,state,operator)-record(alternative,state,operator))
                  for operator,state in product((X,Z),old_states))
    new_gap = record(candidate,old_states[2],Y)-record(alternative,old_states[2],Y)
    return dict(theta=theta, old_menu_gap=old_gap, new_quadrature_gap=new_gap,
                full_output_trace_distance=float(abs(np.sin(theta))))


def environment_reference():
    overlap = .35
    environment_a = np.array([overlap,np.sqrt(1-overlap**2)])
    environment_b = Z@environment_a
    initial_environment = np.array([1.,0.])
    joint = [np.r_[initial_environment,environment]/np.sqrt(2.) for environment in (environment_a,environment_b)]
    states = [np.outer(ket,ket) for ket in joint]
    output = [np.trace(state.reshape(2,2,2,2),axis1=1,axis2=3) for state in states]
    env_x = [float(np.trace(state@np.kron(I,X))) for state in states]
    env_z = [float(np.trace(state@np.kron(I,Z))) for state in states]
    return dict(output_trace_norm_difference=float(np.linalg.norm(output[0]-output[1],ord='nuc')),
                calibrated_environment_x=env_x, population_only_environment_z=env_z,
                conjugated_measurement_gap=abs(env_x[0]+env_x[1]))


def environment_interventions():
    cnot = np.eye(4)[[0,1,3,2]]
    joint = BELL
    incoherent = np.diag(np.diag(BELL))
    coherent_values, classical_values = [], []
    for pulse in (X,Z):
        evolution = cnot@np.kron(I,pulse)
        for state, record in ((joint,coherent_values),(incoherent,classical_values)):
            output = evolution@state@evolution.T
            record.append(float(np.trace(output@np.kron(X,I))))
    return dict(pulse_labels=['X','Z'], coherent_system_x=coherent_values, incoherent_system_x=classical_values,
                initial_local_population_gap=float(np.max(abs(np.diag(joint)-np.diag(incoherent)))))


def instrument_relabeling():
    system = np.array([1.,1.])/np.sqrt(2.)
    state = np.kron(system,np.array([1.,0.]))
    swap = np.eye(4)[[0,2,1,3]]
    # Apply ordinary storage, rotate its basis, then recover the logical qubit.
    basis_change = np.kron(I,X)
    hidden_pulse = np.kron(I,np.diag([1.,np.exp(.65j)]))
    stages = (swap,hidden_pulse,swap)
    transformed = tuple(basis_change@stage@basis_change for stage in stages)
    instruments = {label: [(I+sign*axis)/2 for sign in (1,-1)] for label,axis in [('X',X),('Y',Y),('Z',Z)]}
    def traces(initial, operations, probe_hidden):
        records = []
        for first_axis in instruments.values():
            for outcome, measurement in enumerate(first_axis):
                early = np.kron(measurement,I)@operations[0]@initial
                after_pulse = operations[1]@early
                feedback = np.kron(Z if outcome else I,I)
                for final_axis in instruments.values():
                    for final in final_axis:
                        k = np.kron(final,probe_hidden)@feedback@operations[2]@after_pulse
                        records.append(float(np.vdot(k,k).real))
        return np.array(records)
    ordinary = traces(state,stages,I)
    relabeled = traces(basis_change@state,transformed,I)
    hidden_zero_projector = (I+Z)/2
    labeled_probe = traces(basis_change@state,transformed,hidden_zero_projector)
    ordinary_probe = traces(state,stages,hidden_zero_projector)
    return dict(record_count=len(ordinary), largest_normalization_error=float(np.max(abs(ordinary.reshape(3,2,3,2).sum(axis=(1,3))-1))),
                largest_record_gap=float(np.max(abs(ordinary-relabeled))),
                fixed_hidden_reference_gap=float(np.max(abs(ordinary_probe-labeled_probe))))


def run():
    return {
        'v5.32': damping_threshold(), 'v5.33': bell_correlations(), 'v5.34': two_basis_benchmark(),
        'v5.35': misregistered_axes(), 'v5.36': reset_residual(), 'v5.37': flagged_erasure(),
        'v5.38': phase_probe(), 'v5.39': environment_reference(), 'v5.40': environment_interventions(),
        'v5.41': instrument_relabeling(),
    }


if __name__ == '__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
