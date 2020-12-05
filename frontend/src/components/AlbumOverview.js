import React from 'react';
import { capture_image_to_album } from './../server'
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardMedia from '@material-ui/core/CardMedia';
import Grid from '@material-ui/core/Grid';
import CameraIcon from '@material-ui/icons/PhotoCamera';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(1),
  },
  emptyAlbumContainer: {
    width: "450px",
  },
  emptyAlbumText: {
    fontWeight: "200"
  },
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  heroButtons: {
    marginTop: theme.spacing(4),
  },
  cardGrid: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(8),
    minHeight: "55vh"
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
  cardMedia: {
    paddingTop: '56.25%', // 16:9
  },
  cardContent: {
    flexGrow: 1,
  }
}));

function AlbumOverview({ albumData, setAlbumData }) {
  const [isCapturingImage, setIsCapturingImage] = React.useState(false);
  const classes = useStyles();
  const thumbnailUrls = albumData.thumbnail_urls
  const imageUrls = albumData.image_urls
  const albumName = albumData.album_name
  const albumDescription = albumData.description

  let cardGrid = null
  if (thumbnailUrls.length === 0) {
    cardGrid = (
      <Container className={classes.emptyAlbumContainer}>
        <Typography variant="h3" className={classes.emptyAlbumText} align="center" color="textSecondary" gutterBottom>
          Album is empty :(
        </Typography>
        <Typography variant="h5" className={classes.emptyAlbumText} align="center" color="textSecondary" paragraph>
          There are currently no images in this album. Add an image by pushing the blue button above!
        </Typography>
      </Container>
          )
  } else {
    cardGrid = (
      <Grid container spacing={4}>
        { thumbnailUrls.map((url) => (
          <Grid item key={url} xs={12} sm={6} md={4}>
            <Card className={classes.card}>
              <CardMedia
                className={classes.cardMedia}
                image={url}
                title="No description provided"
              />
              <CardActions>
                <Button size="small" color="primary">
                  View in full size
                </Button>
              </CardActions>
            </Card>
          </Grid>
          ))}
      </Grid>
    )
  }

  const handleClick = async (e) => {
    e.preventDefault();
    setIsCapturingImage(true)
    const response = await capture_image_to_album(albumName)
    setAlbumData({
      album_name: albumName,
      description: albumDescription,
      thumbnail_urls: [response.thumbnailUrls, ...thumbnailUrls],
      image_urls: [response.imageUrls, ...imageUrls],
    })
    setIsCapturingImage(false)
  }

  let captureButton = null
  if (!isCapturingImage) {
    captureButton = (
      <Button onClick={e => handleClick(e)} variant="contained" color="primary">
        <CameraIcon className={classes.icon} />
        Capture new image to album
      </Button>
    )
  } else {
    captureButton = <CircularProgress/>
  }

  return (
    <>
      <div className={classes.heroContent}>
        <Container maxWidth="sm">
          <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
            { albumName }
          </Typography>
          <Typography variant="h5" align="center" color="textSecondary" paragraph>
            { albumDescription }
          </Typography>
          <div className={classes.heroButtons}>
            <Grid container spacing={2} justify="center">
              { captureButton }
            </Grid>
          </div>
        </Container>
      </div>
      <Container className={classes.cardGrid} maxWidth="md">
        { cardGrid }
      </Container>
    </>
  );
}

export default AlbumOverview
