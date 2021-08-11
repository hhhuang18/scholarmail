import argparse
import scholarmail.get_email as get_email
import scholarmail.gen_html as gen_html
import webbrowser
import os


def main():
    parser = argparse.ArgumentParser(
        description='a tool for convert google scholar mail to html.')
    parser.add_argument('--conf', type=str,
                        help='configure file', required=True)
    parser.add_argument('--html', type=str,
                        help='export html file', required=True, default='./')
    args = parser.parse_args()
    # path = os.path.abspath(os.path.dirname(__file__))

    name_csv, df = get_email.get_email(args.conf)
    if not df.empty:
        gen_html.gen_html(name_csv, args.conf, args.html, df)
        web_addr = 'file://' + \
            os.path.abspath(os.path.join(args.html, name_csv + '.html'))
        webbrowser.open(web_addr)

        print('Generated html file:')
        print(web_addr)
    else:
        print('No scholar emails')



if __name__ == '__main__':
    main()
