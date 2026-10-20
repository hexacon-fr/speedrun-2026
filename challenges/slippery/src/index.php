<?php

if (isset($_GET['flag'])) {
    header('Content-Type: text/plain');
    if (file_exists(__DIR__ . '/give_flag.txt')) {
        echo file_get_contents('/flag');
    } else {
        echo "give_flag.txt not found in this directory. Nothing to give you.\n";
    }
    exit;
}

$uploadDir = __DIR__ . '/uploads/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

$message = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['archive'])) {
    $file = $_FILES['archive'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $message = 'Upload failed.';
    } elseif (strtolower(pathinfo($file['name'], PATHINFO_EXTENSION)) !== 'zip') {
        $message = 'Only .zip archives are accepted.';
    } else {
        $zip = new ZipArchive();
        if ($zip->open($file['tmp_name']) !== true) {
            $message = 'Could not open the archive.';
        } else {
            $written = [];
            $blocked = [];

            for ($i = 0; $i < $zip->numFiles; $i++) {
                $name = $zip->getNameIndex($i);

                // Skip directory entries.
                if (substr($name, -1) === '/') {
                    continue;
                }

                // Security check: never write PHP files to disk.
                $ext = strtolower(pathinfo($name, PATHINFO_EXTENSION));
                if (in_array($ext, ['php', 'phtml', 'php3', 'php4', 'php5', 'phar'], true)) {
                    $blocked[] = $name;
                    continue;
                }

                $data = $zip->getFromIndex($i);
                $destination = $uploadDir . $name;

                $destDir = dirname($destination);
                if (!is_dir($destDir)) {
                    mkdir($destDir, 0755, true);
                }

                file_put_contents($destination, $data);
                $written[] = $name;
            }

            $zip->close();

            $message = 'Archive processed. Written: ' . (count($written) ? implode(', ', $written) : 'none');
            if (count($blocked)) {
                $message .= ' | Blocked (php not allowed): ' . implode(', ', $blocked);
            }
        }
    }
}

?>
<!doctype html>
<html>
<head><title>Upload Center</title></head>
<body>
<h1>Archive Upload</h1>
<p>Upload a .zip archive and its contents will be extracted into your upload
folder. PHP files are rejected for your safety.</p>

<?php if ($message): ?>
    <p><strong><?= htmlspecialchars($message) ?></strong></p>
<?php endif; ?>

<form method="post" enctype="multipart/form-data">
    <input type="file" name="archive" accept=".zip" required>
    <button type="submit">Upload</button>
</form>

<p><a href="?flag">Flag page</a></p>
</body>
</html>
