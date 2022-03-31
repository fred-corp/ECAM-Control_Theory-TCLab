import matplotlib.pyplot as plt
import numpy as np

class Controller:
    
  def __init__(self, parameters):
      
    self.parameters = parameters
    self.parameters['Kc'] = parameters['Kc'] if 'Kc' in parameters else 1.0
    self.parameters['Ti'] = parameters['Ti'] if 'Ti' in parameters else 0.0
    self.parameters['Td'] = parameters['Td'] if 'Td' in parameters else 0.0
    self.parameters['alpha'] = parameters['alpha'] if 'alpha' in parameters else 0.0

def Margins(P, C,omega, Show = True):
  
  """
  :P: Process as defined by the class "Process".
    Use the following command to define the default process which is simply a unit gain process:
      P = Process({})
    
    A delay, two lead time constants and 2 lag constants can be added.
    
    Use the following commands for a SOPDT process:
      P.parameters['Kp'] = 1.1
      P.parameters['Tlag1'] = 10.0
      P.parameters['Tlag2'] = 2.0
      P.parameters['theta'] = 2.0
    
    Use the following commands for a unit gain Lead-lag process:
      P.parameters['Tlag1'] = 10.0        
      P.parameters['Tlead1'] = 15.0        
    
  :C: Process as defined by the class "Process".
    Use the following command to define the default process which is simply a unit gain process:
      C = Process({})
    
    A delay, two lead time constants and 2 lag constants can be added.
    
    Use the following commands for a SOPDT process:
      C.parameters['Kc'] = 1.1
      C.parameters['Ti'] = 10.0
      C.parameters['Td'] = 2.0
      C.parameters['alpha'] = 2.0
    
    Use the following commands for a unit gain Lead-lag process:
      C.parameters['Tlag1'] = 10.0        
      C.parameters['Tlead1'] = 15.0        
    
  :omega: frequency vector (rad/s); generated by a command of the type "omega = np.logspace(-2, 2, 10000)".
  :Show: boolean value (optional: default value = True). If Show = True, the Bode diagram is shown. Otherwise Ps (P(j omega)) (vector of complex numbers) is returned.
  
  The function "Bode" generates the Bode diagram of the process P
  """     
  
  s = 1j*omega
  
  # Create params for P
  Ptheta = np.exp(-P.parameters['theta']*s)
  PGain = P.parameters['Kp']*np.ones_like(Ptheta)
  PLag1 = 1/(P.parameters['Tlag1']*s + 1)
  PLag2 = 1/(P.parameters['Tlag2']*s + 1)
  PLead1 = P.parameters['Tlead1']*s + 1
  PLead2 = P.parameters['Tlead2']*s + 1
  
  Ps = np.multiply(Ptheta,PGain)
  Ps = np.multiply(Ps,PLag1)
  Ps = np.multiply(Ps,PLag2)
  Ps = np.multiply(Ps,PLead1)
  Ps = np.multiply(Ps,PLead2)

  # Create params for C
  Cs = C.parameters['Kc']*(1 + (1/C.parameters['Ti'])*s + (C.parameters['Td']*s)/(C.parameters['alpha'] * C.parameters['Td'] * s + 1))

  # Calculate values for Bode diagram of L=P*C
  Ls = np.multiply(Ps,Cs)
  
  
  if Show == True:
  
    fig, (ax_gain, ax_phase) = plt.subplots(2,1)
    fig.set_figheight(12)
    fig.set_figwidth(22)

    gain = 20*np.log10(np.abs(Ls))
    phase = (180/np.pi)*np.unwrap(np.angle(Ls))

    # find index of gain where gain is close to 0
    idx_gain_zero = np.argmin(np.abs(gain))

    # find index of phase where phase is close to -180
    idx_phase_neg180 = np.argmin(np.abs(phase - (-180)))
    
    gainCross = omega[idx_gain_zero]
    phaseCross = omega[idx_phase_neg180]

    print((gainCross, phaseCross))

    # Plot Bode diagram

    ax_gain.set_title('Bode plot of L(s) with phase margin of {}°, and gain margin of {} dB'.format(np.around(180+phase[idx_gain_zero], decimals=3), np.around(gain[idx_phase_neg180], decimals=3)))

    # Gain part

    # Gain margin line
    point1 = [phaseCross, gain[idx_phase_neg180]]
    point2 = [phaseCross, 0]
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    ax_gain.plot(x_values, y_values, label='Gain margin')

    ax_gain.semilogx(omega,gain,label='L(s)')
    ax_gain.axhline(y=0, color='r', linestyle='-', label='0 dB')
    gain_min = np.min(20*np.log10(np.abs(Ls)/5))
    gain_max = np.max(20*np.log10(np.abs(Ls)*5))
    ax_gain.set_xlim([np.min(omega), np.max(omega)])
    ax_gain.set_ylim([gain_min, gain_max])
    ax_gain.set_ylabel('Amplitude |L| [db]')
    ax_gain.legend(loc='best')
  
    # Phase part

    # Phase margin line
    point1 = [gainCross, -180]
    point2 = [gainCross, phase[idx_gain_zero]]
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]
    ax_phase.plot(x_values, y_values, label='Phase margin')

    ax_phase.semilogx(omega, phase, label='L(s)') 
    ax_phase.axhline(y=-180, color='r', linestyle='-', label='-180 deg')
    ax_phase.set_xlim([np.min(omega), np.max(omega)])
    ph_min = np.min((180/np.pi)*np.unwrap(np.angle(Ls))) - 10
    ph_max = np.max((180/np.pi)*np.unwrap(np.angle(Ls))) + 10
    ax_phase.set_ylim([np.max([ph_min, -200]), ph_max])
    ax_phase.set_ylabel(r'Phase $\angle L$ [°]')
    ax_phase.legend(loc='best')
  else:
    return Ls