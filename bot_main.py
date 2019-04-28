import bot_selenium
import check_http_status
import make_log
import random

class bot_main():
    action_num = 4
    wait_time = 5
    wait_time_for_linkcheck = 1
    is_headless = True
    log_root_dir = 'log/'
    log_dir = ''
    url = "http://testerchan.hatenadiary.com/"

    def main(self):
        bot = bot_selenium.BotSelenium(self.log_root_dir)
        status = check_http_status.check_url_http_status()
        bot.run_chrome(self.url, self.is_headless)
        self.log_dir = bot.log_dir
        log = make_log.make_log()

        for i in range(self.action_num):
            value_dic = {}
            value_dic['error_msg'] = ''
            value_dic['no'] = str(i + 1)
            value_dic['current_url'] = bot.current_url()
            value_dic['title'] = bot.get_title()

            #入力があった場合random入力を行ってしまう
            bot.random_input()
            #スクリーンショット（変化前）
            is_ok,  value_dic['sc_path_before'] = bot.save_screenshot()

            #ブラウザログを取得する
            value_dic['log_msg'] = bot.get_browser_log()

            #actionlistを作成する
            action_list = bot.make_action_list(self.url)
            length = bot.get_action_list_length()
            value_dic['link_num'] = str(length)
            #行動できることがあった場合
            if  length != 0 :
                #リンクのステータスチェックを行う
                value_dic['error_msg'] = status.check_url_http_status(action_list, self.wait_time_for_linkcheck)
                #行動を行う
                value_dic['is_change'], value_dic['text'], value_dic['tag'],value_dic['loc'] = bot.click(random.randrange(length))

                #サーバー負荷軽減のための待ち時間
                bot.sleep(self.wait_time)
                
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