import random, json
from colorama import init, Fore

class Forca:
  def __init__(self, life, json_path="words.json"):
    print("init agora")
    self.life = life # ❤️
    self.acertos = []
    self.letras_tentadas = []
    self.json_path = json_path
    self.selected_word = self.get_word()
    init() # colorama
    
  def get_word(self):
    try:
      with open(self.json_path, 'r', encoding="utf-8") as file:
        data_json = json.load(file)
        palavras = data_json["palavras"]
        escolhida = random.choice(palavras)
      return {"unmask": escolhida, "mask": '_'*len(escolhida)}
    except FileNotFoundError:
      print(Fore.RED + "Erro: arquivo 'words.json' não encontrado.")
      exit()
    except json.JSONDecodeError:
      print(Fore.RED + "Erro: o arquivo JSON está mal formatado.")
      exit()
  
  def verify(self, letra):
    word = list(self.selected_word["unmask"])
    success = False
    if letra not in self.letras_tentadas:
      for i in range(len(word)):
        if word[i] == letra and i not in self.acertos:
          self.acertos.append(i)
          success = True
      self.letras_tentadas.append(letra)
      return success
    print(Fore.RED + ">>>>> Você já usou essa letra")

  def unmask(self):
    unmask = list(self.selected_word["unmask"])
    mask = list(self.selected_word["mask"])
    for i in self.acertos:
      mask[i] = unmask[i]
    return mask
  
  def is_game_over(self):
    if len(self.acertos) == len(self.selected_word["unmask"]):
      print(f'====>>> PARABÉNS! VOCÊ ACERTOU A PALAVRA: {self.selected_word["unmask"]}')
      return True
    if self.life == 0:
      print(f'GAME OVER 💀 A palavra era "{self.selected_word["unmask"]}"')
      return True
    return False
  
  def damage(self):
    print(Fore.RED + '\n">>>>> Menos uma vida...')
    self.life -= 1
    return self.life

  def loop(self):
    while not self.is_game_over():
      print('='*50)
      print(f'\n PALAVRA: {self.selected_word["mask"].replace("", "ㅤ")}')
      print(f'\n VIDAS RESTANTES: {"❤️ "*self.life}')
      print(f'\n LETRAS USADAS: {", ".join(self.letras_tentadas)}')
      print(f'\n ==> Digite "sair" para encerrar o jogo')
      user_input = input("\n Escolha uma letra: ")

      if user_input != 'sair':
        if len(user_input) != 1 or not user_input.isalpha():
          print(Fore.YELLOW + '\n>>>>> Escolha uma letra válida!')
          continue
        letra_certa = self.verify(user_input)
        self.damage() if not letra_certa else print(Fore.GREEN + '\n>>>>> Você acertou a letra!')
        self.selected_word["mask"] = ''.join(forca.unmask()) 
      else:
        print(Fore.CYAN + "===>>> JOGO ENCERRADO PELO USUÁRIO")
        break

forca = Forca(5) # o jogo inicia com 5 vidas
forca.loop()
