import React from 'react';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import {
    Link
  } from "react-router-dom";
import { Grid } from '@material-ui/core';
import Logo from '../../assets/logo.png';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
      color: "white",
      textDecoration: 'none',
      fontSize: '18px'
    },
    link: {
        textDecoration: 'none',
        marginLeft: '32px'
    },
    toolbar: {
        display: 'flex',
        justifyContent: 'space-between',
        backgroundColor: '#B82B3F',
    },
    brand: {
      fontWeight: 'bold',
      color: 'white',
      fontSize: '22px'
    }
  }),
);

export function Appbar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static" elevation={0}>
        <Toolbar className={classes.toolbar}>
        <Link to="/" className={classes.link}>
          <Typography variant="subtitle1" className={classes.brand}>
            VoteLink
          </Typography>
          </Link>
          <Grid
            style={{display:'flex'}}
          >
        <Link to="/vote/1" className={classes.link}>
          <Typography variant="subtitle1" className={classes.title}>
            Vote
          </Typography>
          </Link>
          <Link to="/blocks" className={classes.link}>
          <Typography variant="subtitle1" className={classes.title}>
            Blocks
          </Typography>
          </Link>
          </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
}