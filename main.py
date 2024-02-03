from selenium import webdriver
from twitchio.ext import commands
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_experimental_option('excludeSwitches', ['disable-logging'])
chrome_options.add_argument("--log-level=3")

def run_script(nick_to_search):

    # Inicializar o navegador
    driver = webdriver.Chrome(options=chrome_options)

    url = f"https://br.crossfire.z8games.com/competitiveranking.html"

    driver.get(url)

    try:
       if nick_to_search:
            # Inserir o nick na barra de pesquisa
            search_field = driver.find_element(By.ID, "desk_search_text")
            search_field.send_keys(nick_to_search + Keys.RETURN)

            # Esperar pelos resultados da pesquisa
            results_locator = (By.XPATH, "//ul[@class='cfr-rank col-4b']")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(results_locator))

            # Encontrar o elemento que contém o nick desejado na tabela de resultados
            result_element = driver.find_element(By.XPATH, f"//ul[@class='cfr-rank col-4b']//li[@class='cfr-rank-name']/a[contains(text(), '{nick_to_search}')]")
            
            # Extrair o link do atributo href
            profile_link = result_element.get_attribute("href")

            # Imprimir o link
            print(f"\nPerfil do jogador: {profile_link}\n")

            url_profile = profile_link
            driver.get(url_profile)

    except Exception as e:
        print(f"Erro: Jogador não encontrado")

    try:
        # Encontrar o segundo elemento com a classe 'pastseason_pastSeason__X4Bzw'
        season_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "pastseason_pastSeason__X4Bzw"))
        )[1]

        h1_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "PlayerHeader_ign_heading__AT-l_"))
        )

        player_name = h1_element.find_element(By.TAG_NAME, "a").text

        try:
            season_name = season_elements.find_element(By.CLASS_NAME, "pastseason_tierText__3j7pS").find_element(By.TAG_NAME, "h3").text
        except NoSuchElementException:
            season_name = "NÃO ENCONTRADO"

        try:
            modogame = season_elements.find_elements(By.CLASS_NAME, "pastseason_tierText__3j7pS")[1].find_element(By.TAG_NAME, "h5").text
        except NoSuchElementException:
            modogame = "NÃO ENCONTRADO"

        try:
            rank = season_elements.find_elements(By.CLASS_NAME, "pastseason_tierText__3j7pS")[1].find_element(By.TAG_NAME, "h3").text
            rank = rank.replace("#", "")
        except NoSuchElementException:
            rank = "NÃO ENCONTRADO"

        print(f'\n {season_name} - {player_name} - {modogame} - RANK: {rank}º')
        return f'\n {season_name} - {player_name} - {modogame} - RANK: {rank}º'

    except Exception as e:
        print( f"Pesquise novamente! {e}")

    # Fechar o navegador
    driver.quit()

# Bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token='xo6ne1nfecd6m31aj8g9r2hbzuq2ci', client_id='gp762nuuoqcoxypju8c569th9wz7q5', nick='rank', prefix='!', initial_channels=['yuuri_dev', 'zaipzin']) # Tem que ser MOD

    async def event_ready(self):
        print(f'\nOnline | {self.nick}\n')

    @commands.command(name='rank')
    async def elorank(self, ctx, *args):
        if not args:
            await ctx.send('Por favor, forneça o nome do jogador após o comando. Exemplo: !rank jogador1')
        else:
            nick_to_search = ' '.join(args)
            result = run_script(nick_to_search)
            await ctx.send(result)

# Executar o bot
if __name__ == "__main__":
    bot = Bot()
    bot.run()