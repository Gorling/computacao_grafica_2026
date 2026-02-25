import math

#função que calcula a magnitude de um vetor
def calculaMagnitude(x, y, z):
  mag = math.sqrt(x*x + y*y + z*z)
  return mag

#função que soma vetores
def somaVetor(x, y, z, a, b, c):
  v = x + a
  e = y + b
  t = z + c
  return v, e, t

#função que multiplica o vetor por um escalar
def multiplicaVetor(x, y, z, escalar):
  m = x*escalar
  u = y*escalar
  l = z*escalar
  return m, u, l

#função que normatiza o vetor
def normatizaVetor (x, y, z, mag):
  n = x/mag
  o = y/mag
  r = z/mag
  return n, o, r

#função escalar com outro vetor
def escalarVetor (x, y, z, a, b ,c):
  f = x*a
  g = y*b
  h = z*c
  return f, g, h

#menu
while True:
    print("\n" + "="*35)
    print("       MENU DE VETORES")
    print("="*35)
    print("1 - Calcular Magnitude")
    print("2 - Somar Vetores")
    print("3 - Multiplicar Vetor por Escalar")
    print("4 - Normatizar Vetor")
    print("5 - Escalar com outro Vetor")
    print("0 - Sair")
    print("="*35)
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == '0':
        print("Encerrando o programa...")
        break
        
    elif opcao == '1':
        print("\n-- Calcular Magnitude --")
        x = float(input("Digite o valor de X: "))
        y = float(input("Digite o valor de Y: "))
        z = float(input("Digite o valor de Z: "))
        
        mag = calculaMagnitude(x, y, z)
        print(f"A magnitude do vetor é: {mag:.4f}")
        
    elif opcao == '2':
        print("\n-- Somar Vetores --")
        print("Vetor 1:")
        x = float(input("X1: "))
        y = float(input("Y1: "))
        z = float(input("Z1: "))
        print("Vetor 2:")
        a = float(input("X2: "))
        b = float(input("Y2: "))
        c = float(input("Z2: "))
        
        rx, ry, rz = somaVetor(x, y, z, a, b, c)
        print(f"Vetor resultante: ({rx}, {ry}, {rz})")
        
    elif opcao == '3':
        print("\n-- Multiplicar Vetor --")
        x = float(input("Digite o valor de X: "))
        y = float(input("Digite o valor de Y: "))
        z = float(input("Digite o valor de Z: "))
        escalar = float(input("Digite o valor do escalar: "))
        
        rx, ry, rz = multiplicaVetor(x, y, z, escalar)
        print(f"Vetor resultante: ({rx}, {ry}, {rz})")
        
    elif opcao == '4':
        print("\n-- Normatizar Vetor --")
        x = float(input("Digite o valor de X: "))
        y = float(input("Digite o valor de Y: "))
        z = float(input("Digite o valor de Z: "))
        
        # 1º Passo: Chama a magnitude para descobrir o tamanho
        mag = calculaMagnitude(x, y, z)
        
        # Prevenção de erro: não se pode dividir por zero
        if mag == 0:
            print("Erro: Não é possível normatizar um vetor nulo (0, 0, 0) pois sua magnitude é zero.")
        else:
            # 2º Passo: Passa a magnitude calculada para a função de normatizar
            nx, ny, nz = normatizaVetor(x, y, z, mag)
            print(f"Vetor normatizado: ({nx:.4f}, {ny:.4f}, {nz:.4f})")
    elif opcao == '5':
        print("\n-- Escalar com outro Vetor --")
        print("Vetor 1:")
        x = float(input("X1: "))
        y = float(input("Y1: "))
        z = float(input("Z1: "))
        print("Vetor 2:")
        a = float(input("X2: "))
        b = float(input("Y2: "))
        c = float(input("Z2: "))
        
        f, g, h = escalarVetor(x, y, z, a, b, c)
        print(f"Vetor resultante: ({f}, {g}, {h})")
            
    else:
        print("Opção inválida! Tente novamente.")
