from PIL import Image
import os

# A3サイズのピクセル数を横向きで指定（300 DPIで作成）
A3_WIDTH, A3_HEIGHT = 4961, 3508

# 出力フォルダと写真フォルダのパス
photos_folder = './photos'
output_folder = './output'

# 画像を貼り付ける位置を計算（2x3のグリッド）
positions = [
    (0, 0),
    (A3_WIDTH // 3, 0),
    (2 * A3_WIDTH // 3, 0),
    (0, A3_HEIGHT // 2),
    (A3_WIDTH // 3, A3_HEIGHT // 2),
    (2 * A3_WIDTH // 3, A3_HEIGHT // 2),
]

# 余白のサイズを指定
margin = 10

# photosフォルダ内の画像を取得
photo_files = [f for f in os.listdir(photos_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

# 出力フォルダが存在しない場合は作成
os.makedirs(output_folder, exist_ok=True)

# 6枚ずつ処理して出力
for i in range(0, len(photo_files), 6):
    # A3サイズの新しい白紙画像を作成
    a3_image = Image.new('RGB', (A3_WIDTH, A3_HEIGHT), 'white')

    # 6枚の画像を取得
    batch_files = photo_files[i:i+6]

    for j, photo_file in enumerate(batch_files):
        photo_path = os.path.join(photos_folder, photo_file)
        photo = Image.open(photo_path)

        # 画像をリサイズして余白を追加
        target_width = A3_WIDTH // 3 - 2 * margin
        target_height = A3_HEIGHT // 2 - 2 * margin
        aspect_ratio = photo.width / photo.height
        if aspect_ratio > 1:  # 横長の場合
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
        else:  # 縦長の場合
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
        resized_photo = photo.resize((new_width, new_height), Image.LANCZOS)

        # 余白を含むキャンバスを作成し、画像を貼り付け
        canvas = Image.new('RGB', (target_width + 2 * margin, target_height + 2 * margin), 'white')
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        canvas.paste(resized_photo, (x, y))

        # 画像を貼り付ける位置の計算
        x = positions[j][0] + margin
        y = positions[j][1] + margin

        # 画像を貼り付け
        a3_image.paste(canvas, (x, y))

    # 出力ファイル名を連番で作成
    output_file = os.path.join(output_folder, f'output_{i//6 + 1}.png')

    # 完成品をPNGとして出力
    a3_image.save(output_file)
    print(f'完成品が {output_file} に保存されました。')
