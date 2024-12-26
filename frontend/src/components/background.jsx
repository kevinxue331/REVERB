import React, { useRef, useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  PanResponder,
  Animated,
  Dimensions,
  Platform,
} from 'react-native';
import Svg, { Defs, RadialGradient, Rect, Stop, Circle } from 'react-native-svg';

const { width, height } = Dimensions.get('window');

type BackgroundGradientAnimationProps = {
  gradientBackgroundStart?: string;
  gradientBackgroundEnd?: string;
  firstColor?: string;   // "R,G,B" without the "rgba()" or "rgb()"
  secondColor?: string;
  thirdColor?: string;
  fourthColor?: string;
  fifthColor?: string;
  pointerColor?: string;
  size?: number;         // e.g. 0.8 for 80% (we can interpret)
  blendingValue?: string; // Not used in RN; can't replicate mix-blend-mode
  interactive?: boolean;
  children?: React.ReactNode;
};

/**
 * A simplified React Native version of the web-based
 * background gradients animation. This uses react-native-svg
 * to render radial gradients, plus an optional animated “pointer” circle.
 *
 * Note: Many browser-only features (mix-blend-mode, SVG filters) are not
 * natively available in RN. This is a starting point, not a drop-in replacement.
 */
export const BackgroundGradientAnimation: React.FC<
  BackgroundGradientAnimationProps
> = ({
  gradientBackgroundStart = '#6C00A2',
  gradientBackgroundEnd = '#001152',
  firstColor = '200,213,255',
  secondColor = '221,174,255',
  thirdColor = '100,220,255',
  fourthColor = '200,150,250',
  fifthColor = '180,180,150',
  pointerColor = '250,250,255',
  size = 0.8, // interpret as 80% of screen
  blendingValue = 'hard-light', // can't replicate in RN
  interactive = true,
  children,
}) => {
  // Convert “R,G,B” to something like rgba(R,G,B, alpha)
  const toRgba = (rgb: string, alpha: number) => `rgba(${rgb},${alpha})`;

  // Center positions
  const centerX = width / 2;
  const centerY = height / 2;

  // We'll store the "pointer" position in an Animated.ValueXY
  const pointerPos = useRef(new Animated.ValueXY({ x: centerX, y: centerY })).current;

  // PanResponder for interactive pointer
  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => interactive,
      onMoveShouldSetPanResponder: () => interactive,
      onPanResponderMove: (evt, gestureState) => {
        // We can animate pointer to the current touch
        Animated.spring(pointerPos, {
          toValue: { x: gestureState.moveX, y: gestureState.moveY },
          useNativeDriver: false,
        }).start();
      },
      onPanResponderRelease: () => {},
    })
  ).current;

  // If we want a subtle "float" effect similar to your web code, you can do
  // an interpolation in an animation loop. 
  // For brevity, we’ll do direct spring updates from the PanResponder.

  const circleSize = Math.min(width, height) * size;

  return (
    <View style={[styles.container]}>
      {/* 
        We’ll create a background with two big Rects or linear gradients, 
        because a real vertical or diagonal gradient is simpler with 
        react-native-linear-gradient. For demonstration, let's just use a 
        plain background color. 
      */}
      <View
        style={[
          StyleSheet.absoluteFill,
          {
            backgroundColor: gradientBackgroundStart,
          },
        ]}
      />

      {/* 
        Now let's place multiple radial gradients using <Svg />. 
        Each <Circle> with a <RadialGradient> can mimic one "blob".
      */}
      <Svg
        pointerEvents="none"
        height={height}
        width={width}
        style={StyleSheet.absoluteFill}
      >
        <Defs>
          {/* 
            We define multiple radial gradients. 
            Each has an id, used by one Circle. 
            (Alpha set to ~0.8 at center, 0 at edges, to mimic your gradient fade-out)
          */}
          <RadialGradient id="grad1" cx="50%" cy="50%" r="50%">
            <Stop offset="0" stopColor={toRgba(firstColor, 0.8)} />
            <Stop offset="1" stopColor={toRgba(firstColor, 0)} />
          </RadialGradient>
          <RadialGradient id="grad2" cx="50%" cy="50%" r="50%">
            <Stop offset="0" stopColor={toRgba(secondColor, 0.8)} />
            <Stop offset="1" stopColor={toRgba(secondColor, 0)} />
          </RadialGradient>
          <RadialGradient id="grad3" cx="50%" cy="50%" r="50%">
            <Stop offset="0" stopColor={toRgba(thirdColor, 0.8)} />
            <Stop offset="1" stopColor={toRgba(thirdColor, 0)} />
          </RadialGradient>
          <RadialGradient id="grad4" cx="50%" cy="50%" r="50%">
            <Stop offset="0" stopColor={toRgba(fourthColor, 0.8)} />
            <Stop offset="1" stopColor={toRgba(fourthColor, 0)} />
          </RadialGradient>
          <RadialGradient id="grad5" cx="50%" cy="50%" r="50%">
            <Stop offset="0" stopColor={toRgba(fifthColor, 0.8)} />
            <Stop offset="1" stopColor={toRgba(fifthColor, 0)} />
          </RadialGradient>
        </Defs>

        {/* 
          Each Circle below is “centered” in the screen with some offset, 
          similar to your `top-[calc(50%-var(--size)/2)] left-[calc(50%-var(--size)/2)]`. 
          We use `cx`, `cy`, and `r` to define the radial area. 
        */}
        <Circle
          cx={centerX}
          cy={centerY}
          r={circleSize * 0.5}
          fill="url(#grad1)"
        />
        <Circle
          cx={centerX - 100}
          cy={centerY - 200}
          r={circleSize * 0.4}
          fill="url(#grad2)"
        />
        <Circle
          cx={centerX + 150}
          cy={centerY + 50}
          r={circleSize * 0.4}
          fill="url(#grad3)"
        />
        <Circle
          cx={centerX - 200}
          cy={centerY + 150}
          r={circleSize * 0.3}
          fill="url(#grad4)"
        />
        <Circle
          cx={centerX + 250}
          cy={centerY - 100}
          r={circleSize * 0.5}
          fill="url(#grad5)"
        />
      </Svg>

      {/* 
        Interactive pointer “blob”. This is an Animated.View that we place 
        where the user touches. We use a radial gradient with react-native-svg 
        or simply a View with a background color. 
        Below, we show a large Animated.View with a semi-transparent background.
      */}
      {interactive && (
        <Animated.View
          {...panResponder.panHandlers}
          style={[
            styles.pointer,
            {
              transform: [
                { translateX: Animated.subtract(pointerPos.x, 100) }, // center the blob
                { translateY: Animated.subtract(pointerPos.y, 100) },
              ],
              backgroundColor: toRgba(pointerColor, 0.4),
            },
          ]}
        />
      )}

      {/* 
        Place your children above everything if you want 
        text or other components on top of the background 
      */}
      <View style={styles.contentContainer}>{children}</View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  pointer: {
    position: 'absolute',
    width: 200,
    height: 200,
    borderRadius: 100,
  },
  contentContainer: {
    ...StyleSheet.absoluteFillObject,
    // For demonstration, center children
    justifyContent: 'center',
    alignItems: 'center',
  },
});
