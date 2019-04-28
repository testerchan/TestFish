import bot_selenium
import check_http_status
import make_log
import use_yaml
import random

class bot_main():
    action_num = 4
    wait_time = 5
    wait_time_for_linkcheck = 1
    is_headless = True
    is_link_check = True
    is_browser_check = True
    log_root_dir = 'log/'
    log_dir = ''
    url = "http://example.selenium.jp/reserveApp/"
    

    def __init__(self):
        self.load('settings.txt')

    def load(self, path):
        yaml = use_yaml.use_yaml().load_csv(path)
        self.action_num = int(yaml['ActuatingCycle'])
        self.wait_time = int(yaml['WaitTimeForAction'])
        self.wait_time_for_linkcheck = float(yaml['WaitTimeForLinkCheck'])
        self.is_headless = True if yaml['IsHeadless'] == 'True' else False
        self.is_link_check = True if yaml['IsLinkCheck'] == 'True' else False
        self.is_browser_check = True if yaml['IsBrowserCheck'] == 'True' else False
        self.log_root_dir = yaml['LogDir']
        self.url = yaml['TargetUrl']


    def main(self):
        bot = bot_selenium.BotSelenium(self.log_root_dir)
        status = check_http_status.check_url_http_status()
        bot.run_chrome(self.url, self.is_headless)
        self.log_dir = bot.log_dir
        log = make_log.make_log()

        for i in range(self.action_num):
            value_dic = {}
            value_dic['error_msg'] = ''
            value_dic['log_msg'] = ''
            value_dic['no'] = str(i + 1)
            value_dic['current_url'] = bot.current_url()
            value_dic['title'] = bot.get_title()
            bot.set_origin_code()

            #入力があった場合random入力を行ってしまう
            bot.random_input()
            #スクリーンショット（変化前）
            is_ok,  value_dic['sc_path_before'] = bot.save_screenshot()

            #ブラウザログを取得する
            if self.is_browser_check :
                value_dic['log_msg'] = bot.get_browser_log()

            #actionlistを作成する
            action_list = bot.make_action_list(self.url)
            length = bot.get_action_list_length()
            value_dic['link_num'] = str(length)
            #行動できることがあった場合
            if  length != 0 :
                #リンクのステータスチェックを行う
                if self.is_link_check :
                    value_dic['error_msg'] = status.check_url_http_status(action_list, self.wait_time_for_linkcheck)
                #行動を行う
                value_dic['text'], value_dic['tag'],value_dic['loc'] = bot.click(random.randrange(length))

                #サーバー負荷軽減のための待ち時間
                bot.sleep(self.wait_time)

                value_dic['is_change'] = bot.is_change_html_source()
                
                #スクリーンショット（変化後）
                is_ok, value_dic['sc_path_after'] = bot.save_screenshot()

                #アラートは消す
                is_alert = bot.alert_ok()
                
            else:
                break
            #ログの保存
            log.save_log(value_dic, self.log_dir)

        bot.close()


if __name__ == '__main__':
    m = bot_main()
    m.main()