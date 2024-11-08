### 仮想環境を新しく作り直す手順

1. **既存の仮想環境を削除**
    - まず、作成済みの仮想環境フォルダ（例えば`venv/`）を削除するよ。
    - プロジェクトフォルダ内で以下のコマンドを実行して削除するか、フォルダを手動で削除してね。
        
        ```bash
        bash
        Copy code
        rm -rf venv/
        
        ```
        
2. **仮想環境の再作成**
    - 新しい仮想環境を作成する。プロジェクトフォルダに移動して、次のコマンドを実行するよ。
        
        ```bash
        bash
        Copy code
        python -m venv venv
        
        ```
        
3. **仮想環境を有効化**
    - 作成した仮想環境を有効にするよ。
        - **Windows**:
            
            ```bash
            bash
            Copy code
            .\venv\Scripts\activate
            
            ```
            
        - **Linux/Mac**:
            
            ```bash
            bash
            Copy code
            source venv/bin/activate
            
            ```
            
4. **`requirements.txt` からライブラリをインストール**
    - 仮想環境が有効な状態で、`requirements.txt`に記載されているライブラリをインストールする。
        
        ```bash
        bash
        Copy code
        pip install -r requirements.txt
        
        ```
