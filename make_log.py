import utility

class make_log():
    header = ('<!DOCTYPE html><html><head>'
    '<link href="../../items/css.css" rel="stylesheet" type="text/css">'
    '</head><body>')
    footer = '</body></html>'

    all_message = ''

    def __init__(self):
        self.all_message += self.header

    def save_log(self, value_dic, log_dir):
        self.all_message += self.add_scenario_header(value_dic)
        self.all_message += self.add_left_column(value_dic)
        self.all_message += '<div class="right_column">'
        self.all_message += self.add_basic_info(value_dic)
        self.all_message += self.add_action_info(value_dic)
        self.all_message += self.add_browser_log(value_dic)
        self.all_message += self.add_status_log(value_dic)
        self.all_message += '</div>'
        self.all_message += '<div class="clear"></div>'
        self.all_message += '</div>'
        utility.utility().save_file(log_dir + '/index.html', self.all_message + self.footer)
        return

    #タイトル部分
    def add_scenario_header(self, value_dic):
        text = \
            (
                '<div class="main_template">'
                '<div class="title shadow">'
            )
        if value_dic['is_change'] == '変化なし':
            text += '<img class="icon" src="../../items/ng.png">'
        if value_dic['error_msg'] != '' or value_dic['log_msg'] != '':
            text += '<img class="icon" src="../../items/denger.png">'
        text += '#' + value_dic['no'] + '(' + value_dic['current_url'] + ')'
        text += '</div>'
        return text

    #画像部分
    def add_left_column(self, value_dic):
        text = \
            (
                '<div class="left_column">'
                '<div class="origin_img">'
                '<div class="title shadow">'
                '行動前'
            )
        word = utility.utility().get_last_ward_of_url(value_dic['sc_path_before'])
        text += '<a href="' + word + '" target="_blank">'
        text += '<img class="img_size" src="' + word + '">'
        text += '</a></div></div>'
        text += '<div class="origin_img"><div class="title shadow">行動後'
        word = utility.utility().get_last_ward_of_url(value_dic['sc_path_after'])
        text += '<a href="' + word + '" target="_blank">'
        text += '<img class="img_size" src="' + word + '">'
        text += '</a></div></div></div>'
        return text

    #ベーシックインフォメーション
    def add_basic_info(self, value_dic):
        text = \
            (
                '<div class="basic_info contents_template">'
                '<div class="title shadow">'
                'ページ情報'
                '</div>'
            )
        text += self.add_contents('URL', value_dic['current_url'])
        text += self.add_contents('タイトル', value_dic['title'])
        text += self.add_contents('リンク＆ボタン総数', value_dic['link_num'])
        text += '</div>'
        return text

    #action_info
    def add_action_info(self, value_dic):
        text = \
            (
                '<div class="action_info contents_template">'
                '<div class="title shadow">'
                '行ったアクション'
                '</div>'
            )
        text += self.add_contents('結果', value_dic['is_change'])
        text += self.add_contents('テキスト', value_dic['text'])
        text += self.add_contents('タグ', value_dic['tag'])
        text += self.add_contents('要素の座標', value_dic['loc'])
        text += '</div>'
        return text
        
    def add_contents(self, title, content):
        text = '<div class="small_title">'
        text += title + '</div>'
        text += '<div class="content">'
        text += content + '</div>'
        return text

    def add_browser_log(self, value_dic):
        text = \
            (
                '<div class="browser_log contents_template">'
                '<div class="title shadow">'
                'ブラウザログ'
                '</div>'
            )
        text += self.add_textarea(value_dic['log_msg'])
        text += '</div>'
        return text
    
    def add_status_log(self, value_dic):
        text = \
            (
                '<div class="status_log contents_template">'
                '<div class="title shadow">'
                'リンク先確認'
                '</div>'
            )
        text += self.add_textarea(value_dic['error_msg'])
        text += '</div>'
        return text

    def add_textarea(self, message):
        text = \
            (
                '<div class="small_title">'
                '結果'
                '</div>'
                '<div class="content">'
                '<textarea class="textarea_size">'
            )
        text += message + '</textarea></div>'
        return text

