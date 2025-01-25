const fileInput = document.getElementById('fileInput');
        const compressBtn = document.getElementById('compressBtn');
        const decompressBtn = document.getElementById('decompressBtn');
        const downloadSection = document.getElementById('downloadSection');
        const downloadLink = document.getElementById('downloadLink');

        const backendUrl = 'https://127.0.0.1:8000'; // Update this if your backend runs on a different URL

        const uploadFile = async (endpoint) => {
            const file = fileInput.files[0];
            if (!file) {
                alert('Please select a file first.');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch(`${backendUrl}/${endpoint}`, {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error('Failed to process the file.');
                }

                const data = await response.json();
                const filePath = data.compressed_file || data.decompressed_file;

                // Show the download link
                downloadSection.style.display = 'block';
                downloadLink.href = `${backendUrl}/download/${filePath}`;
                downloadLink.innerText = filePath.split('/').pop();
            } catch (error) {
                alert('An error occurred: ' + error.message);
            }
        };

        compressBtn.addEventListener('click', () => uploadFile('compress'));
        decompressBtn.addEventListener('click', () => uploadFile('decompress'));