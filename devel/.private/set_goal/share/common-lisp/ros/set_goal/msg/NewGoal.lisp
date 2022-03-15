; Auto-generated. Do not edit!


(cl:in-package set_goal-msg)


;//! \htmlinclude NewGoal.msg.html

(cl:defclass <NewGoal> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0)
   (theta
    :reader theta
    :initarg :theta
    :type cl:float
    :initform 0.0))
)

(cl:defclass NewGoal (<NewGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <NewGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'NewGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name set_goal-msg:<NewGoal> is deprecated: use set_goal-msg:NewGoal instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <NewGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader set_goal-msg:x-val is deprecated.  Use set_goal-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <NewGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader set_goal-msg:y-val is deprecated.  Use set_goal-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'theta-val :lambda-list '(m))
(cl:defmethod theta-val ((m <NewGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader set_goal-msg:theta-val is deprecated.  Use set_goal-msg:theta instead.")
  (theta m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <NewGoal>) ostream)
  "Serializes a message object of type '<NewGoal>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'theta))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <NewGoal>) istream)
  "Deserializes a message object of type '<NewGoal>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'theta) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<NewGoal>)))
  "Returns string type for a message object of type '<NewGoal>"
  "set_goal/NewGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'NewGoal)))
  "Returns string type for a message object of type 'NewGoal"
  "set_goal/NewGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<NewGoal>)))
  "Returns md5sum for a message object of type '<NewGoal>"
  "a130bc60ee6513855dc62ea83fcc5b20")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'NewGoal)))
  "Returns md5sum for a message object of type 'NewGoal"
  "a130bc60ee6513855dc62ea83fcc5b20")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<NewGoal>)))
  "Returns full string definition for message of type '<NewGoal>"
  (cl:format cl:nil "float32 x~%float32 y~%float32 theta~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'NewGoal)))
  "Returns full string definition for message of type 'NewGoal"
  (cl:format cl:nil "float32 x~%float32 y~%float32 theta~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <NewGoal>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <NewGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'NewGoal
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':theta (theta msg))
))
