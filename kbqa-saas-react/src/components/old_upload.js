import React from 'react'
// import 'antd/dist/antd.css'
import { Upload, message, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const props = {
  name: 'file',
  multiple: false,
  action: 'http://localhost:5000/upload',
  onChange(info) {
      const { status } = info.file;
      if (status !== 'uploading') {
          console.log(info.file, info.fileList);
      }

      if (status === 'done') {
          message.success(`${info.file.name} file uploaded successfully.`);
      } else if (status === 'error') {
          message.error(`${info.file.name} file upload failed.`);
      }
  },
};

// const data = new FormData();
//     data.append('file', this.uploadInput.files[0]);
//     data.append('filename', this.fileName.value);

//     fetch('http://localhost:8000/upload', {
//       method: 'POST',
//       body: data,
//     }).then((response) => {
//       response.json().then((body) => {
//         this.setState({ imageURL: `http://localhost:8000/${body.file}` });
//       });
//     });

export default class UploadProcess extends React.Component
{   
    render() {
        return(  
        <Upload {...props}>
            <Button>
              <UploadOutlined /> Click to Upload
            </Button>
          </Upload>
        )
    }

}
