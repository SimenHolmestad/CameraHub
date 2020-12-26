import React from 'react';
import QrCodePage from './QrCodePage';
import LastImage from './LastImage';

function QrCodeLastImagePage(props) {
  const albumName = props.match.params.albumName
  return (
    <>
      <LastImage albumName={albumName} overlay={true} overlayTime={20000}/>
      <QrCodePage/>
    </>
  );
}

export default QrCodeLastImagePage
