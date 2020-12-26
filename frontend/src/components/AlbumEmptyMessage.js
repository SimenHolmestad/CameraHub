import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

const useStyles = makeStyles(() => ({
  noImagesDiv: {
    height: "90vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center"
  }
}));

function AlbumEmptyMessage() {
  const classes = useStyles();
  return (
    <div className={ classes.noImagesDiv }>
      <Container justify="center" maxWidth="sm">
        <Typography variant="h3" className={classes.emptyAlbumText} align="center" color="textSecondary" gutterBottom>
          There are no images
        </Typography>
        <Typography variant="h5" className={classes.emptyAlbumText} align="center" color="textSecondary" paragraph>
          There are currently no images in this album. Images will appear here when they are captured to the album.
        </Typography>
      </Container>
    </div>
  );
}

export default AlbumEmptyMessage
