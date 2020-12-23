import React from 'react';
import { get_qr_codes } from './../server'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import CameraIcon from '@material-ui/icons/PhotoCamera';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button'
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom';


const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  logo: {
    textDecoration: "inherit",
    color: "inherit",
    textTransform: "none"
  },
  qrCodeGridItem: {
    width: "45%"
  },
  image: {
    width: "100%"
  },
  qrCodeGrid: {
    marginTop: "5%"
  }
}));

function QrCodePage() {
  const classes = useStyles();
  const [qrCodeData, setQrCodeData] = React.useState([]);
  React.useEffect(() => {
    async function fetchData() {
      const response = await get_qr_codes()
      setQrCodeData(response.qr_codes)
    }
    fetchData()
  }, []);

  const qrCodes = qrCodeData.map((qrCode, index) => (
    <Grid item key={index} className={classes.qrCodeGridItem}>
      <img className={classes.image}
           src={qrCode.url}
           alt={qrCode.name}/>
      <Typography variant="h6" align="center">
        {qrCode.information}
      </Typography>
    </Grid>
  ))

  return (
    <>
      <AppBar position="relative">
        <Toolbar>
          <Button component={Link} to={ "/" } className={classes.logo}>
            <CameraIcon className={classes.icon} />
            <Typography variant="h6" color="inherit" noWrap>
              CameraHub
            </Typography>
          </Button>
        </Toolbar>
      </AppBar>
      <Grid container justify="space-around" className={classes.qrCodeGrid}>
        {qrCodes}
      </Grid>
    </>
  );
}

export default QrCodePage
