# Libs

# Lead-Lag


# Constrain
def constrain(val, min_val, max_val):
  return min(max_val, max(min_val, val))

# PID
def PID(PV, SP, MV, Ts, Kc, Ti, Td, alpha, approximationType, man=False, manMV=[0], MVmin=0, MVmax=100):
  """
  parameters : 
  • PV : array of all recorded PV values
  • SP : current SP value
  • MV : dict of all recorded MV ({"MV" : [0], "MVp" : [0], "MVi": [0], "MVd": [0], "E" : [0]})
  • Ts : Sample time (seconds)
  • Kc : PID gain
  • Ti : PID Integration time constant
  • Td : PID Derivation time constant
  • alpha : proportional parameter between Td and Tfd
  • approximationType : list of approximation types for integration and derivation ( looks like : ["EBD", "TRAP"])
  • man : boolean, true if manual mode is enabled
  • manMV : array of manual MV values
  • MVmin : minimum value of MV (default : 0)
  • MVmax : maximum value of MV (default : 100)
  
  """
  try : 
    MVi_previous = MV["MVi"][-1]
  except :
    MVi_previous = 0
  
  try : 
    MVd_previous = MV["MVd"][-1]
  except :
    MVd_previous = 0
  
  try : 
    E_previous = MV["E"][-1]
  except :
    E_previous = 0

  E = SP - PV[-1]

  Tfd = alpha * Td

  # Proportional term
  MVp = Kc * E

  # Intergation term
  if approximationType[0] == "TRAP":
    MVi = MVi_previous + ((Kc*Ts)/(2*Ti)) * (E + E_previous)
  elif approximationType[0] == "EBD":
    MVi = MVi_previous + ((Kc*Ts)/Ti) * E

  # Derivative term
  if approximationType[1] == "TRAP":
    MVd = ((Tfd-(Ts/2))/(Tfd+(Ts/2))) * MVd_previous + ((Kc*Td)/(Tfd+(Ts/2))) * (E - E_previous)
  elif approximationType[1] == "EBD":
    MVd = (Tfd/(Tfd+Ts)) * MVd_previous + ((Kc*Td)/(Tfd+Ts)) * (E - E_previous)
  
  # Manual mode ?
  if man :
    MVi = constrain(manMV[-1], MVmin, MVmax) - MVp - MVd
  else :
    if (MVp + MVi + MVd) > MVmax :
      MVi = MVmax - MVp
    if (MVp + MVi + MVd) < MVmin :
      MVi = MVmin - MVp

  # Calculate MV
  MV = MVp + MVi + MVd

  output = {"MV": MV, "MVp": MVp, "MVi": MVi, "MVd": MVd, "E": E}
  return output


# FF
def FF(P, D, gamma):
  # P & D are dictionaries with parameters : K, T1, T2, Theta

  gain = - D["K"] / P["K"]



  pass