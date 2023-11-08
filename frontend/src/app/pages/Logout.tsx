import { logout } from '../slices/userSlice';
import { useAppDispatch } from '../hooks';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const Logout = (): null => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    void dispatch(logout());
    navigate('/');
  }, []);

  return null;
};

export default Logout;
