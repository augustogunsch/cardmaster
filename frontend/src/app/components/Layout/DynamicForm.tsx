import React from 'react';

import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import {
  Button,
  Container,
  Dialog,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Slide
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import type { TransitionProps } from '@mui/material/transitions';

export interface IProps {
  open: boolean
  handleClose: () => void
  handleSubmit: () => void
  title: string
  children: React.JSX.Element | React.JSX.Element[]
}

const Transition = React.forwardRef(function Transition (
  props: TransitionProps & {
    children: React.ReactElement
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const DynamicForm = ({
  open,
  handleClose,
  handleSubmit,
  title,
  children
}: IProps): React.JSX.Element => {
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down('md'));

  return (
      <Dialog
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
        fullScreen={fullScreen}
        maxWidth="md"
        fullWidth
      >
        <AppBar position="sticky">
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              {title}
            </Typography>
            <Button autoFocus color="inherit" onClick={handleSubmit}>
              save
            </Button>
          </Toolbar>
        </AppBar>
        <Container
          sx={{
            padding: 4
          }}
        >
          {children}
        </Container>
      </Dialog>
  );
};

export default DynamicForm;
