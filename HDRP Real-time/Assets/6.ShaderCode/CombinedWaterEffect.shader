Shader "Custom/CombinedWaterEffect"
{
    Properties
    {
        _Color ("Tint Color", Color) = (1,1,1,1)

        // Vertex Waving
        _Amplitude ("Wave Amplitude", Range(0,4)) = 1.0
        _Movement ("Wave Movement Speed", Range(-100,100)) = 1.0

        // Textures
        _MainTex ("Main texture", 2D) = "white" {}
        _NoiseTex ("Noise texture", 2D) = "grey" {}

        // Distortion
        _Mitigation ("Distortion Mitigation", Range(1, 30)) = 10
        _SpeedX ("Speed X", Range(0, 5)) = 1
        _SpeedY ("Speed Y", Range(0, 5)) = 1
    }

    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            // Vertex wave params
            float _Amplitude;
            float _Movement;

            // Textures + distortion
            sampler2D _MainTex;
            sampler2D _NoiseTex;
            float4 _MainTex_ST;
            float _Mitigation;
            float _SpeedX;
            float _SpeedY;
            float4 _Color;

            struct v2f
            {
                float4 pos : SV_POSITION;
                float2 uv  : TEXCOORD0;
            };

            v2f vert(appdata_base v)
            {
                v2f o;

                // Convert vertex to world space
                float4 worldPos = mul(unity_ObjectToWorld, v.vertex);

                // Generate vertex waves
                float displacement =
                    cos(worldPos.y) +
                    cos(worldPos.x + _Movement * _Time.y);

                worldPos.y += _Amplitude * displacement;

                // Transform back to clip space
                o.pos = mul(UNITY_MATRIX_VP, worldPos);

                // UV setup
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                return o;
            }

            fixed4 frag(v2f i) : COLOR
            {
                float2 uv = i.uv;

                // Sample noise
                float noiseVal = tex2D(_NoiseTex, uv).r;

                // UV distortion
                uv.x += noiseVal * sin(_Time.y * _SpeedX) / _Mitigation;
                uv.y += noiseVal * sin(_Time.y * _SpeedY) / _Mitigation;

                // Sample water texture
                fixed4 col = tex2D(_MainTex, uv);

                return col * _Color;
            }

            ENDCG
        }
    }

    FallBack "Diffuse"
}
