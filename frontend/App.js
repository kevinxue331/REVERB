import React from 'react';
import { Text, View } from 'react-native';
import { BackgroundGradientAnimation } from './src/components/background.jsx';
import tailwind from 'tailwind-rn';

export default function App() {
  return (
    <BackgroundGradientAnimation>
      <View style={tailwind('flex-1 justify-center items-center')}>
        <Text style={tailwind('text-4xl text-white font-bold')}>REVERB</Text>
      </View>
    </BackgroundGradientAnimation>
  );
}