from app import app, db, QandA

# アプリケーションコンテキストを設定
with app.app_context():
    # データベースの作成
    db.drop_all()  # 既存のデータベースを削除
    db.create_all()

    # 初期データの追加
    initial_data = [
        {
            'question': '製品を初めて使うのですが、基本的な操作方法を教えてください。',
            'answer': '弊社Webサイトの製品ページにあるユーザーマニュアルをはじめにご確認ください。電源の入れ方、各ボタンの機能、初期設定の方法などが詳しく解説されています。わからない点があればお問い合わせフォームからご質問ください。',
            'is_template': True,
            'is_confirmed': False
        },
        {
            'question': 'エラーメッセージが表示されて操作できません。どうすればいいですか?',
            'answer': 'エラー番号とメッセージの内容を控えてサポートセンターまでご連絡ください。原因を調査し、解決方法をご案内いたします。',
            'is_template': True,
            'is_confirmed': False
        },
        {
            'question': '製品のウィルス対策はどのようになっていますか?',
            'answer': '弊社のセキュリティソフトウェアにより、各種ウィルスからの検出と駆除を実施しています。定期的にパターンファイルの更新も行っており、最新の脅威から製品を保護しております。',
            'is_template': True,
            'is_confirmed': False
        },
        {
            'question': 'パスワードを忘れてしまったのですが、どうすれば再設定できますか?',
            'answer': 'パスワード再設定はユーザー登録時のメールアドレス宛に専用URLを送信することで実施できます。画面の案内に従って新しいパスワードをご設定ください。',
            'is_template': True,
            'is_confirmed': False
        }
    ]

    for data in initial_data:
        new_qa = QandA(question=data['question'], answer=data['answer'], is_template=data['is_template'], is_confirmed=data['is_confirmed'])
        db.session.add(new_qa)

    db.session.commit()