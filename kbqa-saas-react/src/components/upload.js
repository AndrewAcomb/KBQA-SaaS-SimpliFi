import React from 'react'
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import reqwest from 'reqwest';
import 'antd/es/message/style/css'; // for css
import 'antd/es/upload/style/css'; // for css


export default class UploadProcess extends React.Component {
  state = {
    fileList: [],
    uploading: false,
    uploaded_once: false,
  };

  handleUpload = () => {
    this.props.uploadedPassback();

    const { fileList } = this.state;
    const formData = new FormData();
    fileList.forEach(file => {
      formData.append('file', file);
    });

    this.setState({
      uploading: true,
      uploaded_once: true,
    });

    // You can use any AJAX library you like
    reqwest({
      url: 'http://localhost:5000/upload',
      method: 'post',   
      processData: false,
      data: formData,
      success: () => {
        this.setState({
          fileList: [],
          uploading: false,
        });
        console.log('upload successfully')
        message.success('upload successfully.');
      },
      error: () => {
        this.setState({
          uploading: false,
        });
        console.log('upload failed')
        message.error('upload failed.');
      },
    });
  };

  render() {
    const { uploading, fileList } = this.state;
    const props = {
      onRemove: file => {
        this.setState(state => {
          const index = state.fileList.indexOf(file);
          const newFileList = state.fileList.slice();
          newFileList.splice(index, 1);
          return {
            fileList: newFileList,
          };
        });
      },
      beforeUpload: file => {
        this.setState(state => ({
          fileList: [...state.fileList, file],
        }));
        return false;
      },
      fileList,
    };

    if (this.state.uploaded_once == true) return null;
    return (
      <div>
        <Upload {...props}>
          <Button>
            <UploadOutlined /> Select File
          </Button>
        </Upload>
        <Button
          type="primary"
          onClick={this.handleUpload}
          disabled={fileList.length === 0}
          loading={uploading}
          style={{ marginTop: 16 }}
        >
          {uploading ? 'Uploading' : 'Start Upload'}
        </Button>
      </div>
    );
  }
}