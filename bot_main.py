import bot_selenium
import check_http_status
import random

class bot_main():
    wait_time = 5
    wait_time_for_linkcheck = 1
    is_headless = False
    log_root_dir = 'log/'
    url = "http://testerchan.hatenadiary.com/"

    def main(self):
        bot = bot_selenium.BotSelenium(self.log_root_dir)
        status = check_http_status.check_url_http_status()
        bot.run_chrome(self.url, self.is_headless)

        for i in range(2):

            #入力があった場合random入力を行ってしまう
            bot.random_input()
            #スクリーンショット（変化前）
            is_ok, sc_path = bot.save_screenshot()

            #ブラウザログを取得する
            log_list = bot.get_browser_log()

            #actionlistを作成する
            action_list = bot.make_action_list(self.url)
            length = bot.get_action_list_length()
            #行動できることがあった場合
            if  length != 0 :
                #リンクのステータスチェックを行う
                error_list = status.check_url_http_status(
                    action_list, 
                    self.wait_time_for_linkcheck
                )
                #行動を行う
                is_change, text, tag, loc = bot.click(random.randrange(length))

                #サーバー負荷軽減のための待ち時間
                bot.sleep(self.wait_time)
                
                #スクリーンショット（変化後）
                is_ok, sc_path = bot.save_screenshot()
                print("isok:" + str(is_ok))

                #アラートは消す
                is_alert = bot.alert_ok()
                
            else:
                break
        bot.close()


if __name__ == '__main__':
    m = bot_main()
    m.main()