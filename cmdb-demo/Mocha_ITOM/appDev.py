from oms import create_app

app = create_app("development")  # 生产模式

if __name__ == '__main__':
    app.run()
