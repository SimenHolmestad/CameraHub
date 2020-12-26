import React from 'react';
import LastImage from './LastImage'

function LastImagePage(props) {
  return (
    <LastImage albumName={props.match.params.albumName}/>
  );
}

export default LastImagePage
