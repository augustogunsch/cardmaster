import React from 'react';
import { useAppSelector } from '../hooks';
import Login from '../pages/Login';

export interface IProps {
  children: React.JSX.Element | React.JSX.Element[]
}

const LoggedIn = ({ children }: IProps): React.JSX.Element => {
  const userStatus = useAppSelector(state => state.user.status);

  if (userStatus === 'initial') {
    return <></>;
  }

  if (userStatus === 'loaded') {
    return <>{children}</>;
  }

  return <Login />;
};

export default LoggedIn;
