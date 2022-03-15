# Libs

# Lead-Lag


# Constrain
def constrain(val, min_val, max_val):
  return min(max_val, max(min_val, val))

# PID
def PID(Ts, previous, E, Kc, Ti, Td, alpha, approximationType, man=False, manMV=0, MVmin=0, MVmax=100):
  """
  parameters : 
  • Ts : Sample time (seconds)
  • previous : dictionary with previous values for MVi, MVd, E (looks like : {"MVi": 0, "MVd": 0, "E": 0})
  • E : difference between PV and SP
  • Kc : PID gain
  • Ti : PID Integration time constant
  • Td : PID Derivation time constant
  • alpha : 
  • approximationType : list of approximation types for integration and derivation ( looks like : ["EBD", "TRAP"])
  • man : boolean, true if manual mode is enabled
  • manMV : manual MV value
  • MVmin : minimum value of MV (default : 0)
  • MVmax : maximum value of MV (default : 100)
  
  """    
  # previous is a dict with parameters : MVi, MVd, E
  MVi_previous = previous["MVi"]
  MVd_previous = previous["MVd"]
  E_previous = previous["E"]

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
    MVi = constrain(manMV, MVmin, MVmax) - MVp - MVd
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