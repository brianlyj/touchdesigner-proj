uniform vec4 uEye; // xyz, tan(horizontal fov/2)
uniform vec4 uRight; // xyz, aspect
uniform vec4 uUp;
uniform vec4 uForward;
in vec3 worldPosition;
out vec4 fragColor;
vec3 cameraPoint(vec3 p){vec3 d=p-uEye.xyz;return vec3(dot(d,uRight.xyz),dot(d,uUp.xyz),dot(d,uForward.xyz));}
