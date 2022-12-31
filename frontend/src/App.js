import React, { useState } from 'react';
import './App.css';

import {
  Button,
  message,
  Upload,
} from 'antd';
import {
  DownloadOutlined,
  UploadOutlined,
} from '@ant-design/icons';

const baseUrl = process.env.ENDPOINT || 'http://localhost:8000';

// const getJson = async (path) => {
//   fetch(`${baseUrl}/${path}/`)
//   .then(response => {
//     if (response.ok) {
//       return response.json();
//     }
//   })
//   .then(responseJson => {
//     console.log(responseJson);
//   })
//   .catch(error => {
//     console.error(error);
//   })
// }

const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

const getFile = async (path) => {
  fetch(`${baseUrl}/${path}/`)
  .then(response => {
    if (response.ok) {
      return response.blob();
    }
  })
  .then(blob => {
    downloadBlob(blob, 'example.csv');
  })
  .catch(error => {
    console.error(error);
  })
}

const donwloadExample = () => {
  getFile('example');
};

function App() {
  const [fileList, setFileList] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('includesN', true);
    fileList.forEach((file) => {
      formData.append('file', file);
    });
    setUploading(true);
    fetch(`${baseUrl}/upload/`, {
      method: 'POST',
      body: formData,
    })
      .then((res) => res.json())
      .then(() => {
        setFileList([]);
        message.success('upload successfully.');
      })
      .catch(() => {
        message.error('upload failed.');
      })
      .finally(() => {
        setUploading(false);
      });
  };

  const uploadProps = {
    onRemove: (file) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },
    _beforeUpload: (file) => {
      const isMultipleFiles = false;
      if (isMultipleFiles) {
        setFileList([...fileList, file]);
      } else {
        setFileList([file]);
      }

      return false;
    },
    get beforeUpload_1() {
      return this._beforeUpload;
    },
    set beforeUpload_1(value) {
      this._beforeUpload = value;
    },
    get beforeUpload() {
      return this._beforeUpload;
    },
    set beforeUpload(value) {
      this._beforeUpload = value;
    },
    fileList,
  };

  return (
    <div className="App">
      <Button
        type="primary"
        shape="round"
        icon={<DownloadOutlined />}
        size="large"
        onClick={donwloadExample}
      >
      Downnload
      </Button>

      <div>
        <Upload {...uploadProps}>
          <Button icon={<UploadOutlined />}>Select</Button>
        </Upload>
        <Button
          type="primary"
          onClick={handleUpload}
          disabled={fileList.length === 0}
          loading={uploading}
          style={{ marginTop: 16 }}
        >
          {uploading ? 'Uploading' : 'Start Upload'}
        </Button>
      </div>
    </div>
  );
}

export default App;
