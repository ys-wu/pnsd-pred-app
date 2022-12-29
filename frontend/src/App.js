import './App.css';

import {
  Button,
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

const uploadProps = {
  action: `${baseUrl}/inputs/`,
  onChange({ file, fileList }) {
    if (file.status !== 'uploading') {
      console.log(file, fileList);
    }
  },
};

function App() {
  return (
    <div className="App">
      <Button
        type="primary"
        shape="round"
        icon={<DownloadOutlined />}
        size="large"
        onClick={donwloadExample}
      >
        Download example.csv
      </Button>
      <Upload {...uploadProps}>
        <Button icon={<UploadOutlined />}>Upload</Button>
      </Upload>
    </div>
  );
}

export default App;
